import os

# Safe local placeholder only — never put real credentials here, this file
# is committed. Point DATABASE_URL at a real test database via the actual
# environment (e.g. `DATABASE_URL=... uv run pytest`) to run against it.
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db_test")
os.environ.setdefault("JWT_SECRET", "test-secret")

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text

from app.db.session import engine
from app.main import app


@pytest.fixture
async def async_client():
    """Talks to the ASGI app in-process via httpx, in the *same* event loop
    pytest-asyncio is running this test in. Deliberately not Starlette's
    TestClient — TestClient runs the app in its own separate event loop,
    which fights with the async SQLAlchemy engine's loop-bound connection
    pool the moment a fixture and a request try to use it from different
    loops (`attached to a different loop` from asyncpg)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
async def clean_users_table():
    """Explicit, not autouse — test_health.py has no DB dependency and
    should keep working even without a reachable database (e.g. CI without
    the DATABASE_URL secret configured). Only tests that touch users opt in."""
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE TABLE users CASCADE"))
    yield