import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class TurnCreate(BaseModel):
    role: Literal["question", "answer"]
    content: str


class TurnOut(BaseModel):
    id: uuid.UUID
    interview_id: uuid.UUID
    turn_number: int
    role: Literal["question", "answer"]
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}