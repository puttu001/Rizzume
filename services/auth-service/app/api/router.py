from fastapi import APIRouter

from app.api import auth

# No prefix here — api-gateway forwards /api/v1/auth/{path} to this
# service's /{path} directly (see api-gateway/app/api/endpoints/auth.py).
api_router = APIRouter()
api_router.include_router(auth.router)
