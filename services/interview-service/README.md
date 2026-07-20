# interview-service

Session/interview logic and the OpenAI interview engine (`app/engine/`).
Owns `interview_db`.

## Run locally

```
uv sync
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8002
```

## Test

```
uv run pytest
```

## Status

Infrastructure only so far. `app/engine`, `app/models`, `app/schemas`,
`app/repositories`, `app/services`, `app/api` are empty on purpose — the
actual interview flow (question generation, follow-ups, difficulty,
feedback) is the next piece of work, built deliberately rather than
scaffolded sight-unseen.
