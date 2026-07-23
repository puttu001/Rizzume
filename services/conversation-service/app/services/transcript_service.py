import uuid

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import session_cache, transcript_repository
from app.schemas.transcript import TurnOut


async def get_turns(db: AsyncSession, redis: Redis, interview_id: uuid.UUID) -> list[TurnOut]:
    cached = await session_cache.get_cached_turns(redis, interview_id)
    if cached is not None:
        return cached

    turns = await transcript_repository.get_turns(db, interview_id)
    result = [TurnOut.model_validate(turn) for turn in turns]
    await session_cache.set_cached_turns(redis, interview_id, result)
    return result


async def add_turn(
    db: AsyncSession, redis: Redis, *, interview_id: uuid.UUID, role: str, content: str
) -> TurnOut:
    turn = await transcript_repository.add_turn(
        db, interview_id=interview_id, role=role, content=content
    )
    # Invalidate rather than patch in-place — simpler to reason about than
    # keeping a cached list consistent with a partial update, and the next
    # read repopulates it in one query anyway.
    await session_cache.invalidate(redis, interview_id)
    return TurnOut.model_validate(turn)