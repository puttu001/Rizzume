import uuid

from fastapi import Header, HTTPException, status


async def get_current_user_id(x_user_id: str | None = Header(default=None)) -> uuid.UUID:
    """Trusts api-gateway's X-User-Id header — see auth-service/app/api/deps.py
    for the full rationale. Duplicated here on purpose, not shared: this is
    exactly the kind of small utility the architecture deliberately
    duplicates rather than coupling services through a shared package."""
    if x_user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing X-User-Id")
    try:
        return uuid.UUID(x_user_id)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid X-User-Id"
        ) from exc