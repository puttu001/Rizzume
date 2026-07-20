from fastapi import APIRouter, Request

from app.clients.registry import get_client
from app.core.proxy import proxy_request

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.api_route("/{downstream_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def forward_to_report_service(downstream_path: str, request: Request):
    return await proxy_request(request, get_client("report"), f"/{downstream_path}")
