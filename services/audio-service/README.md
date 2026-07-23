# audio-service

Speech-to-text / text-to-speech. Deliberately has no SQL database — session
and transcript state live in `conversation-service`; this service processes
audio and hands results off.

## Endpoints

- `POST /transcriptions` (multipart audio upload) — uploads to Azure Blob
  Storage, enqueues a Celery transcription job, returns `{job_id, status}`.
  Async on purpose: a candidate's spoken answer can be long enough that a
  synchronous call risks timing out the request.
- `GET /transcriptions/{job_id}` — poll for the result:
  `{job_id, status, transcript}`.
- `POST /speech` (`{text}`) — synchronous, returns audio bytes directly
  (`audio/mpeg`). A single interview question is short enough that the
  job-queue round trip isn't worth it, and the interview flow needs the
  audio back quickly to keep moving.

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

(On Windows, add `--pool=solo`.)

## Test

```
uv run pytest
```

## Status

Built and verified live: real upload → real Azure Blob Storage → real
Celery task (queue `audio_tasks` — see `app/worker/celery_app.py` for why
this, not a numbered Redis DB, is what isolates it from report-service's
worker on the same hosted Redis instance) → real `gpt-4o-mini-transcribe`
call → accurate transcript. `POST /speech` verified against real
`gpt-4o-mini-tts`. Both model names are from architecture.png and confirmed
still current via a real API call.

`app/services` is empty — there's no orchestration logic beyond what's in
`app/api/` and `app/worker/tasks.py` yet; add it if/when this service needs
logic beyond "upload → transcribe" and "text → speech".
