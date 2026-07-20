# audio-service

Speech-to-text / text-to-speech. Deliberately has no SQL database — session
and transcript state live in `conversation-service`; this service processes
audio and hands results off, using Celery so the API never blocks on a slow
STT/TTS call.

## Run locally

```
uv sync
cp .env.example .env
uv run uvicorn app.main:app --reload --port 8004
```

## Run the worker

```
uv run celery -A app.worker.celery_app worker --loglevel=info
```

## Test

```
uv run pytest
```

## Status

Infrastructure only so far — including a working `audio.ping` task to prove
the worker boots and reaches the broker. `app/providers` (OpenAI STT/TTS
adapters), `app/schemas`, `app/services`, `app/api` are empty on purpose —
that's the next piece of work.
