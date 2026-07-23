async def test_upload_creates_pending_job(async_client, mock_blob_upload, mock_transcribe_delay) -> None:
    response = await async_client.post(
        "/transcriptions", files={"file": ("answer.mp3", b"fake-audio-bytes", "audio/mpeg")}
    )
    assert response.status_code == 202
    body = response.json()
    assert body["status"] == "pending"
    assert body["job_id"] == "fake-job-id"

    # The endpoint generates its own UUID-prefixed blob name (not the
    # mock's return value) and uses that same name for both the upload and
    # the task argument — verify they actually match, not just that both
    # were called.
    uploaded_blob_name = mock_blob_upload.call_args.args[0]
    assert uploaded_blob_name.endswith("-answer.mp3")
    mock_transcribe_delay.assert_called_once_with(uploaded_blob_name)


async def test_upload_rejects_empty_file(async_client, mock_blob_upload, mock_transcribe_delay) -> None:
    response = await async_client.post(
        "/transcriptions", files={"file": ("answer.mp3", b"", "audio/mpeg")}
    )
    assert response.status_code == 400
    mock_blob_upload.assert_not_called()


async def test_poll_pending_job(async_client, mock_celery_async_result) -> None:
    mock_celery_async_result["state"] = "PENDING"
    response = await async_client.get("/transcriptions/some-job-id")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "pending"
    assert body["transcript"] is None


async def test_poll_completed_job_returns_transcript(async_client, mock_celery_async_result) -> None:
    mock_celery_async_result["state"] = "SUCCESS"
    mock_celery_async_result["result"] = "This is the transcribed answer."
    response = await async_client.get("/transcriptions/some-job-id")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "completed"
    assert body["transcript"] == "This is the transcribed answer."


async def test_poll_failed_job(async_client, mock_celery_async_result) -> None:
    mock_celery_async_result["state"] = "FAILURE"
    response = await async_client.get("/transcriptions/some-job-id")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "failed"
    assert body["transcript"] is None
