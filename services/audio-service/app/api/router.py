from fastapi import APIRouter

from app.api import speech, transcriptions

# No "/audio" prefix here — api-gateway strips "/api/v1/audio" and forwards
# the remainder verbatim, same pattern as every other service.
api_router = APIRouter()
api_router.include_router(transcriptions.router)
api_router.include_router(speech.router)
