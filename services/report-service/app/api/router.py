from fastapi import APIRouter

# Endpoint modules register themselves here as they're built, e.g.:
#   from app.api import reports
#   api_router.include_router(reports.router)
api_router = APIRouter()
