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
docker compose -f infra/docker-compose.yml up --build
```

One real command — live-verified (real signup/login round trip against the
real Neon database through the gateway). Every service loads its own
`services/<name>/.env`, which already points at the real hosted Neon /
Upstash / Azure Blob Storage instances (there's no local Postgres/Redis/MinIO
container in this compose file — see `infra/docker-compose.yml`'s header
comment for why).

- Frontend: http://localhost:3000
- API gateway: http://localhost:18000
- Individual services (direct, for debugging only — normally reached through
  the gateway): auth :18001, interview :18002, conversation :18003,
  audio :18004
- Host ports are 18000-18004, not 8000-8004: on Windows, Docker Desktop's
  WSL2 backend can reserve 8000-8004 for its own dynamic NAT range, which
  makes `docker compose up` fail with a port-bind permission error. Check
  `netsh interface ipv4 show excludedportrange protocol=tcp` if you hit this
  after changing these back.
- `report-service` is not part of this compose file — nothing in the working
  flow calls it yet, see `current_state.md`.
- Alternative, no Docker required: `./scripts/run-all.ps1` runs every
  service directly via `uv run`/`npm run` in separate windows, on the
  original 8000-8004 ports.

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
