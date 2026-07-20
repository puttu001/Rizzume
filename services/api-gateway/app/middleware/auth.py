import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.config import get_settings
from app.core.constants import PUBLIC_PATHS


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """Verifies the bearer JWT once at the edge. Downstream services trust the
    `X-User-Id` header this sets (see app/core/proxy.py) instead of re-verifying
    the token themselves — see architecture discussion on the gateway trust boundary."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in PUBLIC_PATHS or request.method == "OPTIONS":
            return await call_next(request)

        settings = get_settings()
        auth_header = request.headers.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing bearer token"})

        token = auth_header.removeprefix("Bearer ")
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except jwt.PyJWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        request.state.user_id = payload.get("sub")
        return await call_next(request)
