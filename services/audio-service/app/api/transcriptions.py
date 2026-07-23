import uuid

from celery.result import AsyncResult
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas.audio import TranscriptionJobCreated, TranscriptionStatus
from app.storage import blob_client
from app.worker.celery_app import celery_app
from app.worker.tasks import transcribe_audio

router = APIRouter(prefix="/transcriptions", tags=["transcriptions"])

# Celery's PENDING state means "not yet started OR unknown id" — it can't
# tell the difference. task_track_started=True (set in celery_app.py) at
# least gives us a distinct STARTED state once a worker picks it up.
_STATE_MAP = {
    "PENDING": "pending",
    "STARTED": "started",
    "SUCCESS": "completed",
    "FAILURE": "failed",
}


@router.post("", response_model=TranscriptionJobCreated, status_code=status.HTTP_202_ACCEPTED)
async def create_transcription(file: UploadFile = File(...)) -> TranscriptionJobCreated:
    audio_bytes = await file.read()
    if not audio_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty audio file")

    blob_name = f"{uuid.uuid4()}-{file.filename or 'answer.webm'}"
    blob_client.upload_blob(blob_name, audio_bytes, content_type=file.content_type or "audio/webm")

    task = transcribe_audio.delay(blob_name)
    return TranscriptionJobCreated(job_id=task.id)


@router.get("/{job_id}", response_model=TranscriptionStatus)
async def get_transcription(job_id: str) -> TranscriptionStatus:
    result = AsyncResult(job_id, app=celery_app)
    status_value = _STATE_MAP.get(result.state, "pending")
    transcript = result.result if status_value == "completed" else None
    return TranscriptionStatus(job_id=job_id, status=status_value, transcript=transcript)
