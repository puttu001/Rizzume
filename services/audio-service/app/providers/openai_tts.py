from app.providers.openai_client import get_openai_client

# Named in architecture.png and confirmed still current via a real API call.
MODEL = "gpt-4o-mini-tts"
DEFAULT_VOICE = "alloy"


def synthesize(text: str) -> bytes:
    client = get_openai_client()
    response = client.audio.speech.create(
        model=MODEL, voice=DEFAULT_VOICE, input=text, response_format="mp3"
    )
    return response.read()