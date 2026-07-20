# report-service

Scoring + PDF/JSON feedback generation. Owns `report_db`; a Celery worker
(`app/worker/`) runs report generation as a background job so the API never
blocks on a slow PDF render.

## Run locally

```
uv sync
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8005
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

Infrastructure only so far — including a working `report.ping` task to prove
the worker boots and reaches the broker. `app/generators` (scoring, PDF
layout), `app/models`, `app/schemas`, `app/repositories`, `app/services`,
`app/api` are empty on purpose — that's the next piece of work.
