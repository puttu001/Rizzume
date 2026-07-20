# Rizzume — AI Interview Assistant

Monorepo, microservices backend, independent frontend. See
`personal-docs/architecture.png` for the original system diagram.

## Layout

```
frontend/            Next.js (App Router, TypeScript, Tailwind) — deploys independently
services/
├── api-gateway/      Public entrypoint: JWT verification, CORS, request forwarding
├── auth-service/      Signup/login/JWT — owns auth_db
├── interview-service/ Session logic + OpenAI engine (app/engine/) — owns interview_db
├── conversation-service/ Interview state + transcript — owns conversation_db + Redis
├── audio-service/     STT/TTS, Celery worker — no SQL db, Redis + object storage only
└── report-service/    Scoring + PDF/JSON, Celery worker — owns report_db
infra/                docker-compose.yml, postgres init script
scripts/               bootstrap-env.sh
```

Every service under `services/` is fully independent: its own `pyproject.toml`
and `uv.lock`, its own database, its own Dockerfile. No shared code package —
see the architecture discussion in this repo's history for why, and the
narrow exceptions (`JWT_SECRET` must match between `auth-service` and
`api-gateway`; Redis DB indices are coordinated in `infra/docker-compose.yml`
to avoid collisions).

## Run everything locally

```bash
cp .env.secrets.example .env.secrets   # fill in real values
./scripts/bootstrap-env.sh             # generates every services/*/.env + frontend/.env
docker compose -f infra/docker-compose.yml --env-file .env.secrets up --build
```

- Frontend: http://localhost:3000
- API gateway: http://localhost:8000
- Individual services (direct, for debugging only — normally reached through
  the gateway): auth :8001, interview :8002, conversation :8003, audio :8004,
  report :8005
- MinIO console: http://localhost:9001

## Run a single service without Docker

```bash
cd services/auth-service
uv sync
cp .env.example .env      # or rely on bootstrap-env.sh output
uv run alembic upgrade head   # db-backed services only
uv run uvicorn app.main:app --reload --port 8001
```

## Status

Infrastructure is scaffolded and verified end-to-end: every service installs
real dependencies, boots, passes a real health-check test, lints clean; the
Next.js frontend builds; `docker-compose.yml` is config-validated. Domain
logic (`app/models`, `app/schemas`, `app/repositories`, `app/services`,
`app/api`, `app/engine`, `app/providers`, `app/generators` in each service)
is intentionally empty — that's the next phase of work, built deliberately
rather than scaffolded sight-unseen.

## Hosting frontend and backend separately

`frontend/` and `services/*` share no code and no build step, so they can be
deployed to entirely different platforms (e.g. Vercel for the frontend, a
VPS/Railway/AWS for the backend). The only coupling is two env vars:
`NEXT_PUBLIC_API_URL` on the frontend and `CORS_ALLOWED_ORIGINS` on
`api-gateway`.
