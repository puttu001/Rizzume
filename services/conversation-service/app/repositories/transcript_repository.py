import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transcript import ConversationTurn


async def get_turns(db: AsyncSession, interview_id: uuid.UUID) -> list[ConversationTurn]:
    result = await db.execute(
        select(ConversationTurn)
        .where(ConversationTurn.interview_id == interview_id)
        .order_by(ConversationTurn.turn_number)
    )
    return list(result.scalars().all())


async def add_turn(
    db: AsyncSession, *, interview_id: uuid.UUID, role: str, content: str
) -> ConversationTurn:
    next_turn_number = await db.scalar(
        select(func.coalesce(func.max(ConversationTurn.turn_number), 0) + 1).where(
            ConversationTurn.interview_id == interview_id
        )
    )
    turn = ConversationTurn(
        interview_id=interview_id,
        turn_number=next_turn_number,
        role=role,
        content=content,
    )
    db.add(turn)
    await db.flush()
    await db.refresh(turn)
    await db.commit()
    return turn