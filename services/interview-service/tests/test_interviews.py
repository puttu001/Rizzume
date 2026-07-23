import uuid

from httpx import AsyncClient

from app.engine.interview_engine import NextStepDecision


async def _start(client: AsyncClient, user_id: uuid.UUID, role_title: str = "Backend Engineer"):
    return await client.post(
        "/",
        data={"role_title": role_title},
        files={"resume": ("resume.pdf", b"%PDF-1.4 fake pdf bytes", "application/pdf")},
        headers={"X-User-Id": str(user_id)},
    )


async def test_start_interview_creates_row_and_returns_opening_question(
    async_client, clean_interviews_table, mock_conversation_client, mock_resume_pipeline, mock_engine, user_id
) -> None:
    response = await _start(async_client, user_id)
    assert response.status_code == 201
    body = response.json()
    assert body["remark"] == "Welcome, thanks for joining today."
    assert body["question"] == "Tell me about yourself."
    assert body["interview"]["status"] == "in_progress"
    assert body["interview"]["question_count"] == 1
    assert body["interview"]["max_questions"] == 10
    assert body["interview"]["user_id"] == str(user_id)
    mock_conversation_client["add_turn"].assert_awaited_once()
    mock_resume_pipeline["extract_text"].assert_called_once()
    mock_resume_pipeline["upload_resume"].assert_called_once()


async def test_start_interview_rejects_non_pdf(
    async_client, clean_interviews_table, mock_conversation_client, mock_resume_pipeline, mock_engine, user_id
) -> None:
    response = await async_client.post(
        "/",
        data={"role_title": "Backend Engineer"},
        files={"resume": ("resume.txt", b"plain text resume", "text/plain")},
        headers={"X-User-Id": str(user_id)},
    )
    assert response.status_code == 400
    mock_resume_pipeline["extract_text"].assert_not_called()


async def test_remark_is_never_sent_to_conversation_service(
    async_client, clean_interviews_table, mock_conversation_client, mock_resume_pipeline, mock_engine, user_id
) -> None:
    """The remark is display/speech only — conversation-service (and the
    engine's own follow-up context, and report-service later) should only
    ever see the clean question text, never the small talk around it."""
    await _start(async_client, user_id)
    stored_content = mock_conversation_client["add_turn"].call_args.kwargs["content"]
    assert stored_content == "Tell me about yourself."
    assert "Welcome" not in stored_content


async def test_get_interview_requires_ownership(
    async_client, clean_interviews_table, mock_conversation_client, mock_resume_pipeline, mock_engine, user_id
) -> None:
    start_response = await _start(async_client, user_id)
    interview_id = start_response.json()["interview"]["id"]

    owner_response = await async_client.get(
        f"/{interview_id}", headers={"X-User-Id": str(user_id)}
    )
    assert owner_response.status_code == 200

    other_user = uuid.uuid4()
    stranger_response = await async_client.get(
        f"/{interview_id}", headers={"X-User-Id": str(other_user)}
    )
    assert stranger_response.status_code == 404


async def test_get_unknown_interview_is_404(async_client, clean_interviews_table, user_id) -> None:
    response = await async_client.get(f"/{uuid.uuid4()}", headers={"X-User-Id": str(user_id)})
    assert response.status_code == 404


async def test_health_endpoint_not_shadowed_by_uuid_route(async_client) -> None:
    """Regression test for the real bug found during manual testing: an
    untyped `/{interview_id}` route matched "/health" and 401'd before
    UUID validation ever ran. Now typed as `/{interview_id:uuid}`."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_submit_answer_advances_difficulty_and_count(
    async_client, clean_interviews_table, mock_conversation_client, mock_resume_pipeline, mock_engine, user_id
) -> None:
    start_response = await _start(async_client, user_id)
    interview_id = start_response.json()["interview"]["id"]

    answer_response = await async_client.post(
        f"/{interview_id}/answer",
        json={"answer": "I'm a backend engineer with 5 years of experience."},
        headers={"X-User-Id": str(user_id)},
    )
    assert answer_response.status_code == 200
    body = answer_response.json()
    assert body["remark"] == "Nice, that's a solid approach."
    assert body["question"] == "Follow-up question?"
    assert body["interview"]["current_difficulty"] == "hard"
    assert body["interview"]["question_count"] == 2
    assert body["feedback"] is None


async def test_submit_answer_ending_interview_generates_feedback(
    async_client, clean_interviews_table, mock_conversation_client, mock_resume_pipeline, mock_engine, user_id
) -> None:
    mock_engine["value"] = NextStepDecision(action="end_interview", reasoning="enough signal")

    start_response = await _start(async_client, user_id)
    interview_id = start_response.json()["interview"]["id"]

    answer_response = await async_client.post(
        f"/{interview_id}/answer",
        json={"answer": "That's my final answer."},
        headers={"X-User-Id": str(user_id)},
    )
    assert answer_response.status_code == 200
    body = answer_response.json()
    assert body["remark"] is None
    assert body["question"] is None
    assert body["feedback"]["overall_score"] == 75
    assert body["interview"]["status"] == "completed"
    assert body["interview"]["completed_at"] is not None


async def test_submit_answer_on_completed_interview_is_conflict(
    async_client, clean_interviews_table, mock_conversation_client, mock_resume_pipeline, mock_engine, user_id
) -> None:
    mock_engine["value"] = NextStepDecision(action="end_interview", reasoning="enough signal")

    start_response = await _start(async_client, user_id)
    interview_id = start_response.json()["interview"]["id"]

    await async_client.post(
        f"/{interview_id}/answer", json={"answer": "Done."}, headers={"X-User-Id": str(user_id)}
    )

    second_attempt = await async_client.post(
        f"/{interview_id}/answer",
        json={"answer": "One more?"},
        headers={"X-User-Id": str(user_id)},
    )
    assert second_attempt.status_code == 409