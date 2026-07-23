from fastapi import APIRouter

from app.api import transcripts

# Internal-only service — not reachable through api-gateway (see
# api-gateway/app/api/endpoints/, which only proxies to auth/interview/
# audio/report). Only interview-service calls this, over the private Docker
# network, so there's no auth check here — it trusts the network boundary
# the same way api-gateway trusts the Docker network for X-User-Id.
api_router = APIRouter()
api_router.include_router(transcripts.router)
