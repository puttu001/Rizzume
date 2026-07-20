from fastapi import APIRouter

# Endpoint modules register themselves here as they're built, e.g.:
#   from app.api import sessions, transcripts
#   api_router.include_router(sessions.router)
api_router = APIRouter()
