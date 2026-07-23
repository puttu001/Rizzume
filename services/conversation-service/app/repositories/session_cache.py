import json
import uuid

from redis.asyncio import Redis

from app.schemas.transcript import TurnOut

# Active-session cache: avoids hitting Postgres on every context-building
# read while an interview is in progress. Not a source of truth — Postgres
# is. TTL means an abandoned session's cache just expires; the durable data
# in Postgres is unaffected.
_CACHE_TTL_SECONDS = 60 * 60 * 2  # 2 hours — comfortably longer than one interview


def _cache_key(interview_id: uuid.UUID) -> str:
    return f"session:{interview_id}:turns"


async def get_cached_turns(redis: Redis, interview_id: uuid.UUID) -> list[TurnOut] | None:
    raw = await redis.get(_cache_key(interview_id))
    if raw is None:
        return None
    return [TurnOut.model_validate(item) for item in json.loads(raw)]


async def set_cached_turns(redis: Redis, interview_id: uuid.UUID, turns: list[TurnOut]) -> None:
    payload = json.dumps([turn.model_dump(mode="json") for turn in turns])
    await redis.set(_cache_key(interview_id), payload, ex=_CACHE_TTL_SECONDS)


async def invalidate(redis: Redis, interview_id: uuid.UUID) -> None:
    await redis.delete(_cache_key(interview_id))