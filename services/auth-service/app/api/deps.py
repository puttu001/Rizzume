import uuid

from fastapi import Header, HTTPException, status


async def get_current_user_id(x_user_id: str | None = Header(default=None)) -> uuid.UUID:
    """Trusts the `X-User-Id` header api-gateway attaches after verifying the
    JWT — this service does not re-verify the token itself. Only reachable
    at all because /me isn't in the gateway's PUBLIC_PATHS, so a request
    without a valid token never gets here in the first place; this is a
    defense-in-depth check for direct calls that bypass the gateway (e.g.
    local debugging on :8001)."""
    if x_user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing X-User-Id")
    try:
        return uuid.UUID(x_user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid X-User-Id"
        ) from exc