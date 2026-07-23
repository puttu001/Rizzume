from fastapi import APIRouter

from app.api import interviews

# No prefix here — api-gateway forwards /api/v1/interviews/{path} to this
# service's /interviews/{path} directly (see
# api-gateway/app/api/endpoints/interview.py).
api_router = APIRouter()
api_router.include_router(interviews.router)
