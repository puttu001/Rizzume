import uuid

from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.redis import get_redis
from app.db.session import get_db
from app.schemas.transcript import TurnCreate, TurnOut
from app.services import transcript_service

router = APIRouter(prefix="/interviews/{interview_id}/turns", tags=["transcripts"])


@router.get("", response_model=list[TurnOut])
async def list_turns(
    interview_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> list[TurnOut]:
    return await transcript_service.get_turns(db, redis, interview_id)


@router.post("", response_model=TurnOut, status_code=201)
async def create_turn(
    interview_id: uuid.UUID,
    payload: TurnCreate,
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> TurnOut:
    return await transcript_service.add_turn(
        db, redis, interview_id=interview_id, role=payload.role, content=payload.content
    )