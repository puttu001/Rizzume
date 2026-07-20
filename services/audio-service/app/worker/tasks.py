from app.worker.celery_app import celery_app


@celery_app.task(name="audio.ping")
def ping() -> str:
    """Proves the worker boots and can reach the broker. Replace/extend with
    real transcribe_audio / synthesize_speech tasks once app/providers/ has
    actual STT/TTS logic."""
    return "pong"
