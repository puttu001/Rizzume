import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.clients import conversation_client
from app.core.constants import MAX_QUESTIONS
from app.engine import feedback_generator, interview_engine, question_generator
from app.models.interview import Interview
from app.repositories import interview_repository


class InterviewNotFoundError(Exception):
    pass


class InterviewNotOwnedError(Exception):
    pass


class InterviewAlreadyCompletedError(Exception):
    pass


async def _get_owned_interview(
    db: AsyncSession, interview_id: uuid.UUID, user_id: uuid.UUID
) -> Interview:
    interview = await interview_repository.get_by_id(db, interview_id)
    if interview is None:
        raise InterviewNotFoundError(interview_id)
    if interview.user_id != user_id:
        raise InterviewNotOwnedError(interview_id)
    return interview


async def start_interview(
    db: AsyncSession, *, user_id: uuid.UUID, role_title: str
) -> tuple[Interview, str, str]:
    interview = await interview_repository.create(db, user_id=user_id, role_title=role_title)
    opening = question_generator.generate_opening_question(role_title)
    # Only the clean question text goes to conversation-service — the
    # remark is display/speech only, never part of the stored transcript
    # (which report-service and the engine's own follow-up context read
    # back later; small talk in there is noise, not signal).
    await conversation_client.add_turn(interview.id, role="question", content=opening.question)
    interview = await interview_repository.advance(
        db, interview, new_difficulty=interview.current_difficulty
    )
    return interview, opening.remark, opening.question


async def get_interview(db: AsyncSession, *, interview_id: uuid.UUID, user_id: uuid.UUID) -> Interview:
    return await _get_owned_interview(db, interview_id, user_id)


async def submit_answer(
    db: AsyncSession, *, interview_id: uuid.UUID, user_id: uuid.UUID, answer: str
) -> tuple[Interview, str | None, str | None, dict | None]:
    """Returns (interview, remark, question, feedback). remark/question are
    None once the interview ends — no next question to introduce."""
    interview = await _get_owned_interview(db, interview_id, user_id)
    if interview.status == "completed":
        raise InterviewAlreadyCompletedError(interview_id)

    await conversation_client.add_turn(interview.id, role="answer", content=answer)
    transcript = await conversation_client.get_transcript(interview.id)

    decision = interview_engine.decide_next_step(
        role_title=interview.role_title,
        transcript=transcript,
        current_difficulty=interview.current_difficulty,
        question_count=interview.question_count,
        max_questions=MAX_QUESTIONS,
    )

    # Enforced here too, not just via the prompt — don't rely on the model
    # reliably stopping itself at the limit.
    if decision.action == "end_interview" or interview.question_count >= MAX_QUESTIONS:
        feedback = feedback_generator.generate_feedback(
            role_title=interview.role_title, transcript=transcript
        )
        feedback_dict = feedback.model_dump()
        interview = await interview_repository.complete(db, interview, feedback=feedback_dict)
        return interview, None, None, feedback_dict

    question = decision.question or "Can you elaborate further on your previous answer?"
    # Same reasoning as start_interview — only the clean question goes to
    # conversation-service, the remark is display/speech only.
    await conversation_client.add_turn(interview.id, role="question", content=question)
    interview = await interview_repository.advance(
        db, interview, new_difficulty=decision.difficulty or interview.current_difficulty
    )
    return interview, decision.remark, question, None