from typing import Literal

from pydantic import BaseModel


class TranscriptionJobCreated(BaseModel):
    job_id: str
    status: Literal["pending"] = "pending"


class TranscriptionStatus(BaseModel):
    job_id: str
    status: Literal["pending", "started", "completed", "failed"]
    transcript: str | None = None


class SpeechRequest(BaseModel):
    text: str
