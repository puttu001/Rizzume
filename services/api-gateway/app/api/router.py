from fastapi import APIRouter

from app.api.endpoints import audio, auth, interview, report

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(interview.router)
api_router.include_router(audio.router)
api_router.include_router(report.router)
