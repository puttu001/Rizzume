import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.interview import Interview


async def get_by_id(db: AsyncSession, interview_id: uuid.UUID) -> Interview | None:
    return await db.get(Interview, interview_id)


async def create(
    db: AsyncSession,
    *,
    user_id: uuid.UUID,
    role_title: str,
    max_questions: int,
    resume_text: str,
    resume_blob_name: str,
) -> Interview:
    interview = Interview(
        user_id=user_id,
        role_title=role_title,
        max_questions=max_questions,
        resume_text=resume_text,
        resume_blob_name=resume_blob_name,
    )
    db.add(interview)
    await db.flush()
    await db.refresh(interview)
    await db.commit()
    return interview


async def advance(
    db: AsyncSession, interview: Interview, *, new_difficulty: str
) -> Interview:
    interview.question_count += 1
    interview.current_difficulty = new_difficulty
    await db.flush()
    await db.refresh(interview)
    await db.commit()
    return interview


async def complete(db: AsyncSession, interview: Interview, *, feedback: dict) -> Interview:
    interview.status = "completed"
    interview.feedback = feedback
    interview.completed_at = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(interview)
    await db.commit()
    return interview