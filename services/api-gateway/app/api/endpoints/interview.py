from fastapi import APIRouter, Request

from app.clients.registry import get_client
from app.core.proxy import proxy_request

# Note: creating an interview is POST /api/v1/interviews/ — WITH the
# trailing slash. Without it, this route doesn't match (interview-service's
# create endpoint is its bare root) and FastAPI 307-redirects to the
# trailing-slash form. fetch()/axios follow 307 transparently (method+body
# preserved per spec), but it's an extra round trip — always include the
# trailing slash when calling this endpoint. Verified live.
router = APIRouter(prefix="/api/v1/interviews", tags=["interviews"])


@router.api_route("/{downstream_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def forward_to_interview_service(downstream_path: str, request: Request):
    return await proxy_request(request, get_client("interview"), f"/{downstream_path}")
