import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

# No InterviewCreate model — POST / is multipart (resume file + role_title
# form field), not a JSON body, so FastAPI takes those as separate
# File()/Form() parameters directly on the endpoint instead.


class AnswerSubmit(BaseModel):
    answer: str


class InterviewOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    role_title: str
    status: Literal["in_progress", "completed"]
    current_difficulty: Literal["easy", "medium", "hard"]
    question_count: int
    max_questions: int
    feedback: dict | None
    created_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}


class InterviewStartResponse(BaseModel):
    interview: InterviewOut
    remark: str
    question: str


class AnswerResponse(BaseModel):
    interview: InterviewOut
    remark: str | None = None
    question: str | None = None
    feedback: dict | None = None