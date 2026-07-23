import os

# Safe local placeholders only — never put real credentials here, this file
# is committed. Point DATABASE_URL/REDIS_URL at real instances via the
# actual environment (e.g. `DATABASE_URL=... REDIS_URL=... uv run pytest`).
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/conversation_db_test",
)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.db.redis import get_redis
from app.db.session import engine
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
async def clean_state():
    """Truncates the transcript table and clears any cache keys this test
    session created. Explicit, not autouse, so test_health.py stays
    DB/Redis-independent."""
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE conversation_turns CASCADE"))
    redis = get_redis()
    async for key in redis.scan_iter("session:*"):
        await redis.delete(key)
    yield