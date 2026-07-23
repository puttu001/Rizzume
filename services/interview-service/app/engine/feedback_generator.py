from pydantic import BaseModel, Field

from app.engine.client import MODEL, get_openai_client
from app.engine.types import TranscriptTurn, format_transcript


class InterviewFeedback(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    strengths: list[str]
    areas_for_improvement: list[str]
    summary: str


def generate_feedback(*, role_title: str, transcript: list[TranscriptTurn]) -> InterviewFeedback:
    client = get_openai_client()
    response = client.responses.parse(
        model=MODEL,
        instructions=(
            f"You just finished interviewing a candidate for a {role_title} position. "
            "Based on the full transcript, give a fair, constructive evaluation: an overall "
            "score out of 100, concrete strengths, concrete areas for improvement, and a "
            "short summary."
        ),
        input=format_transcript(transcript),
        text_format=InterviewFeedback,
    )
    return response.output_parsed