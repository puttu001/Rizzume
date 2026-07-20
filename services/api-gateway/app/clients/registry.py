from functools import lru_cache

import httpx

from app.core.config import get_settings


@lru_cache
def _clients() -> dict[str, httpx.AsyncClient]:
    settings = get_settings()
    return {
        "auth": httpx.AsyncClient(base_url=settings.auth_service_url, timeout=10.0),
        "interview": httpx.AsyncClient(base_url=settings.interview_service_url, timeout=30.0),
        "audio": httpx.AsyncClient(base_url=settings.audio_service_url, timeout=60.0),
        "report": httpx.AsyncClient(base_url=settings.report_service_url, timeout=30.0),
    }


def get_client(name: str) -> httpx.AsyncClient:
    return _clients()[name]


async def close_clients() -> None:
    for client in _clients().values():
        await client.aclose()
