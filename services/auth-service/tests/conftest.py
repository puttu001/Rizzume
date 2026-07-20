import os

os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/auth_db_test")
os.environ.setdefault("JWT_SECRET", "test-secret")
