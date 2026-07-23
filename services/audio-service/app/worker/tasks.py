from app.providers import openai_stt
from app.storage import blob_client
from app.worker.celery_app import celery_app


@celery_app.task(name="audio.ping")
def ping() -> str:
    """Proves the worker boots and can reach the broker — a liveness check
    independent of any business logic below."""
    return "pong"


@celery_app.task(name="audio.transcribe")
def transcribe_audio(blob_name: str) -> str:
    """The blob was already uploaded by the endpoint before this task was
    enqueued (see app/api/transcriptions.py) — only the lightweight blob
    name travels through Redis as the task argument, not the audio bytes
    themselves."""
    audio_bytes = blob_client.download_blob(blob_name)
    return openai_stt.transcribe(audio_bytes, filename=blob_name)
