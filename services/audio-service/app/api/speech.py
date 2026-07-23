from fastapi import APIRouter, Response

from app.providers import openai_tts
from app.schemas.audio import SpeechRequest

router = APIRouter(prefix="/speech", tags=["speech"])


@router.post("")
async def synthesize_speech(payload: SpeechRequest) -> Response:
    """Synchronous, unlike transcription — a single interview question is
    short enough that generating its audio doesn't need the job-queue
    machinery, and the interview flow needs it back quickly to keep moving."""
    audio_bytes = openai_tts.synthesize(payload.text)
    return Response(content=audio_bytes, media_type="audio/mpeg")
