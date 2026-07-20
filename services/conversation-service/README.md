# conversation-service

Interview state + transcript. Owns `conversation_db` (Postgres, durable
transcript) and the active-session cache (Redis).

## Run locally

```
uv sync
cp .env.example .env
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8003
```

## Test

```
uv run pytest
```

## Status

Infrastructure only so far. `app/models`, `app/schemas`, `app/repositories`,
`app/services`, `app/api` are empty on purpose — the transcript/session
read-write logic is the next piece of work.
