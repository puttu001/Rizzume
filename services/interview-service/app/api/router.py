from fastapi import APIRouter

# Endpoint modules register themselves here as they're built, e.g.:
#   from app.api import interviews
#   api_router.include_router(interviews.router)
api_router = APIRouter()
