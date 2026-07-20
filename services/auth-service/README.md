# auth-service

Owns user identity: signup, login, JWT issuance/refresh. Owns `auth_db` —
no other service reads or writes it directly.

## Run locally

```
uv sync
cp .env.example .env   # or let scripts/bootstrap-env.sh do this
uv run alembic upgrade head
uv run uvicorn app.main:app --reload --port 8001
```

## Test

```
uv run pytest
```

## Migrations

```
uv run alembic revision --autogenerate -m "add users table"
uv run alembic upgrade head
```

## Status

Infrastructure only so far: config, DB session, health check, migrations
wiring. `app/models`, `app/schemas`, `app/repositories`, `app/services`,
`app/api` are empty on purpose — signup/login/JWT logic is the next piece of
work, not scaffolded sight-unseen.
