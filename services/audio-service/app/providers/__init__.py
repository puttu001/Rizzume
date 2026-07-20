# Swappable STT/TTS adapters, called from app/worker/tasks.py. Planned:
#   openai_stt.py — gpt-4o-transcribe
#   openai_tts.py — gpt-4o-mini-tts
# Kept behind a common interface here so the provider can change without
# touching the task/queue plumbing.
