import uuid
from functools import lru_cache

import httpx

from app.core.config import get_settings
from app.engine.types import TranscriptTurn


@lru_cache
def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(base_url=get_settings().conversation_service_url, timeout=10.0)


async def add_turn(interview_id: uuid.UUID, *, role: str, content: str) -> None:
    response = await _client().post(
        f"/interviews/{interview_id}/turns", json={"role": role, "content": content}
    )
    response.raise_for_status()


async def get_transcript(interview_id: uuid.UUID) -> list[TranscriptTurn]:
    response = await _client().get(f"/interviews/{interview_id}/turns")
    response.raise_for_status()
    return [TranscriptTurn(role=turn["role"], content=turn["content"]) for turn in response.json()]