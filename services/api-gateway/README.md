# api-gateway

Public entrypoint for the frontend. Verifies JWTs issued by `auth-service`,
applies CORS, and forwards requests to internal services on the Docker
network, attaching a trusted `X-User-Id` header so downstream services don't
need to re-verify tokens themselves.

## Run locally

```
uv sync
cp .env.example .env   # or let scripts/bootstrap-env.sh do this
uv run uvicorn app.main:app --reload --port 8000
```

## Test

```
uv run pytest
```

## Routes

Everything under a prefix is forwarded verbatim (method, query, body) to the
matching downstream service:

| Prefix | Forwards to |
|---|---|
| `/api/v1/auth/*` | `auth-service` |
| `/api/v1/interviews/*` | `interview-service` |
| `/api/v1/audio/*` | `audio-service` |
| `/api/v1/reports/*` | `report-service` |

`/api/v1/auth/signup`, `/api/v1/auth/login`, `/api/v1/auth/refresh`, and
`/health` are the only paths that don't require a bearer token — see
`app/core/constants.py`.
