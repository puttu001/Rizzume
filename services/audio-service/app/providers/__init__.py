# STT/TTS adapters.
#   openai_client.py — shared OpenAI client singleton
#   openai_stt.py     — gpt-4o-mini-transcribe
#   openai_tts.py     — gpt-4o-mini-tts
# Both model names are from architecture.png and confirmed still current
# via a real API call — unlike gpt-4o-mini (the general chat model used by
# interview-service's engine), which no longer exists and was replaced with
# gpt-5.4-mini there.