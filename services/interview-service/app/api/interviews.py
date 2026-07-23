import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user_id
from app.db.session import get_db
from app.schemas.interview import AnswerResponse, AnswerSubmit, InterviewOut, InterviewStartResponse
from app.services import interview_service
from app.utils.pdf_extractor import EmptyResumeError

# No "/interviews" prefix here — api-gateway already strips "/api/v1/interviews"
# and forwards the remainder verbatim (see api-gateway/app/api/endpoints/interview.py),
# so this service's own routes are relative to its root, same as auth-service.
router = APIRouter(tags=["interviews"])


@router.post("/", response_model=InterviewStartResponse, status_code=status.HTTP_201_CREATED)
async def start_interview(
    role_title: str = Form(...),
    resume: UploadFile = File(...),
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> InterviewStartResponse:
    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Resume must be a PDF"
        )

    resume_bytes = await resume.read()
    if not resume_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty resume file")

    try:
        interview, remark, question = await interview_service.start_interview(
            db, user_id=user_id, role_title=role_title, resume_bytes=resume_bytes
        )
    except EmptyResumeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return InterviewStartResponse(
        interview=InterviewOut.model_validate(interview), remark=remark, question=question
    )


@router.get("/{interview_id:uuid}", response_model=InterviewOut)
async def get_interview(
    interview_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> InterviewOut:
    try:
        interview = await interview_service.get_interview(
            db, interview_id=interview_id, user_id=user_id
        )
    except interview_service.InterviewNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found") from exc
    except interview_service.InterviewNotOwnedError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found") from exc
    return InterviewOut.model_validate(interview)


@router.post("/{interview_id:uuid}/answer", response_model=AnswerResponse)
async def submit_answer(
    interview_id: uuid.UUID,
    payload: AnswerSubmit,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> AnswerResponse:
    try:
        interview, remark, question, feedback = await interview_service.submit_answer(
            db, interview_id=interview_id, user_id=user_id, answer=payload.answer
        )
    except interview_service.InterviewNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found") from exc
    except interview_service.InterviewNotOwnedError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Interview not found") from exc
    except interview_service.InterviewAlreadyCompletedError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Interview already completed"
        ) from exc

    return AnswerResponse(
        interview=InterviewOut.model_validate(interview),
        remark=remark,
        question=question,
        feedback=feedback,
    )