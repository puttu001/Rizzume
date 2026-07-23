from typing import Literal

from pydantic import BaseModel


class TranscriptTurn(BaseModel):
    role: Literal["question", "answer"]
    content: str


def format_transcript(transcript: list[TranscriptTurn]) -> str:
    return "\n".join(f"{turn.role}: {turn.content}" for turn in transcript)