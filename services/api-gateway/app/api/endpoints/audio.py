from fastapi import APIRouter, Request

from app.clients.registry import get_client
from app.core.proxy import proxy_request

router = APIRouter(prefix="/api/v1/audio", tags=["audio"])


@router.api_route("/{downstream_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def forward_to_audio_service(downstream_path: str, request: Request):
    return await proxy_request(request, get_client("audio"), f"/{downstream_path}")
