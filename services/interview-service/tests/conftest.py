import os

# Safe local placeholders only — never put real credentials here, this file
# is committed. Point DATABASE_URL/AZURE_CONNECTION_STRING at real values
# via the actual environment (e.g. `DATABASE_URL=... uv run pytest`).
os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/interview_db_test"
)
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault(
    "AZURE_CONNECTION_STRING",
    "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=dGVzdA==;EndpointSuffix=core.windows.net",
)

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.db.session import engine
from app.engine.feedback_generator import InterviewFeedback
from app.engine.interview_engine import NextStepDecision
from app.engine.interview_planner import InterviewPlan
from app.main import app


@pytest.fixture
async def async_client():
    """In-process ASGI client sharing this test's event loop — see
    auth-service/tests/conftest.py for why this matters with an async
    SQLAlchemy engine (loop-bound connection pool)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def clean_interviews_table():
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE interviews CASCADE"))
    yield


@pytest.fixture
def mock_conversation_client(monkeypatch):
    """Tests exercise this service's own logic (routing, DB writes, error
    handling) for real against Neon — they don't need a live
    conversation-service. The actual cross-service integration was verified
    manually against a live conversation-service + Neon + real OpenAI calls
    (see current_state.md); mocking it here keeps the suite fast, free, and
    deterministic."""
    add_turn = AsyncMock(return_value=None)
    get_transcript = AsyncMock(return_value=[])
    monkeypatch.setattr("app.services.interview_service.conversation_client.add_turn", add_turn)
    monkeypatch.setattr(
        "app.services.interview_service.conversation_client.get_transcript", get_transcript
    )
    return {"add_turn": add_turn, "get_transcript": get_transcript}


@pytest.fixture
def mock_resume_pipeline(monkeypatch):
    """Real PDF extraction and Azure upload were verified live (see
    current_state.md) — mocked here so tests don't need a real PDF file or
    Azure connectivity."""
    extract_text = MagicMock(return_value="Experienced backend engineer, 5 years Python.")
    upload_resume = MagicMock(return_value="fake-resume-blob.pdf")
    monkeypatch.setattr("app.services.interview_service.extract_text", extract_text)
    monkeypatch.setattr("app.services.interview_service.blob_client.upload_resume", upload_resume)
    return {"extract_text": extract_text, "upload_resume": upload_resume}


@pytest.fixture
def mock_engine(monkeypatch):
    """Same reasoning as mock_conversation_client — the real OpenAI calls
    were verified manually (see current_state.md); mocked here for a fast,
    free, deterministic suite."""

    def plan_interview(**kwargs):
        return InterviewPlan(
            question_count=10,
            remark="Welcome, thanks for joining today.",
            question="Tell me about yourself.",
            reasoning="test",
        )

    monkeypatch.setattr(
        "app.services.interview_service.interview_planner.plan_interview", plan_interview
    )

    decision_holder = {
        "value": NextStepDecision(
            action="ask_question",
            remark="Nice, that's a solid approach.",
            question="Follow-up question?",
            difficulty="hard",
            reasoning="test",
        )
    }

    def decide_next_step(**kwargs):
        return decision_holder["value"]

    monkeypatch.setattr(
        "app.services.interview_service.interview_engine.decide_next_step", decide_next_step
    )

    def generate_feedback(**kwargs):
        return InterviewFeedback(
            overall_score=75,
            strengths=["Clear communication"],
            areas_for_improvement=["More depth needed"],
            summary="Solid overall performance.",
        )

    monkeypatch.setattr(
        "app.services.interview_service.feedback_generator.generate_feedback", generate_feedback
    )

    return decision_holder


@pytest.fixture
def user_id() -> uuid.UUID:
    return uuid.uuid4()