from fastapi import APIRouter

# Endpoint modules register themselves here as they're built, e.g.:
#   from app.api import transcribe, synthesize
#   api_router.include_router(transcribe.router)
api_router = APIRouter()
