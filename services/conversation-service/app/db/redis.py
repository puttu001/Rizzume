from functools import lru_cache

from redis.asyncio import Redis

from app.core.config import get_settings


@lru_cache
def get_redis() -> Redis:
    """FastAPI dependency: `redis: Redis = Depends(get_redis)`. Holds the
    active-session cache — the durable transcript still lives in Postgres."""
    return Redis.from_url(get_settings().redis_url, decode_responses=True)
