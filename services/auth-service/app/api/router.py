from fastapi import APIRouter

# Endpoint modules register themselves here as they're built, e.g.:
#   from app.api import signup, login
#   api_router.include_router(signup.router)
api_router = APIRouter()
