import io

from app.providers.openai_client import get_openai_client

# Named in architecture.png and confirmed still current via a real API call
# (unlike gpt-4o-mini, the general chat model, which no longer exists).
MODEL = "gpt-4o-mini-transcribe"


def transcribe(audio_bytes: bytes, *, filename: str) -> str:
    client = get_openai_client()
    file_obj = io.BytesIO(audio_bytes)
    file_obj.name = filename  # OpenAI uses the extension to detect format
    return client.audio.transcriptions.create(
        model=MODEL, file=file_obj, response_format="text"
    )