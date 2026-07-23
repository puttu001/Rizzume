import os

# Safe local placeholder only — never put real credentials here, this file
# is committed. Point DATABASE_URL at a real test database via the actual
# environment (e.g. `DATABASE_URL=... uv run pytest`).
os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/interview_db_test"
)
os.environ.setdefault("OPENAI_API_KEY", "test-key")

import uuid
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.db.session import engine
from app.engine.feedback_generator import InterviewFeedback
from app.engine.interview_engine import NextStepDecision
from app.engine.question_generator import OpeningQuestion
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
def mock_engine(monkeypatch):
    """Same reasoning as mock_conversation_client — the real OpenAI calls
    were verified manually (see current_state.md); mocked here for a fast,
    free, deterministic suite."""
    def generate_opening_question(role_title):
        return OpeningQuestion(remark="Welcome, thanks for joining today.", question="Tell me about yourself.")

    monkeypatch.setattr(
        "app.services.interview_service.question_generator.generate_opening_question",
        generate_opening_question,
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