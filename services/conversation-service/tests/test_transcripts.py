import uuid

from httpx import AsyncClient

from app.db.redis import get_redis


async def _add_turn(client: AsyncClient, interview_id: uuid.UUID, role: str, content: str):
    return await client.post(f"/interviews/{interview_id}/turns", json={"role": role, "content": content})


async def test_add_and_list_turns_in_order(async_client, clean_state) -> None:
    interview_id = uuid.uuid4()

    first = await _add_turn(async_client, interview_id, "question", "Tell me about yourself.")
    assert first.status_code == 201
    assert first.json()["turn_number"] == 1

    second = await _add_turn(async_client, interview_id, "answer", "I'm a backend engineer.")
    assert second.status_code == 201
    assert second.json()["turn_number"] == 2

    listed = await async_client.get(f"/interviews/{interview_id}/turns")
    assert listed.status_code == 200
    turns = listed.json()
    assert [t["turn_number"] for t in turns] == [1, 2]
    assert [t["role"] for t in turns] == ["question", "answer"]


async def test_list_turns_for_unknown_interview_is_empty(async_client, clean_state) -> None:
    response = await async_client.get(f"/interviews/{uuid.uuid4()}/turns")
    assert response.status_code == 200
    assert response.json() == []


async def test_turns_from_different_interviews_dont_mix(async_client, clean_state) -> None:
    interview_a = uuid.uuid4()
    interview_b = uuid.uuid4()

    await _add_turn(async_client, interview_a, "question", "Question for A")
    await _add_turn(async_client, interview_b, "question", "Question for B")

    turns_a = (await async_client.get(f"/interviews/{interview_a}/turns")).json()
    turns_b = (await async_client.get(f"/interviews/{interview_b}/turns")).json()

    assert len(turns_a) == 1
    assert len(turns_b) == 1
    assert turns_a[0]["content"] == "Question for A"
    assert turns_b[0]["content"] == "Question for B"


async def test_second_read_is_served_from_cache(async_client, clean_state) -> None:
    """Not just 'does it return the right data twice' — actually confirms
    the cache got populated, since that's the part with real bug potential
    (cache/DB drift, stale TTL, serialization round-trip)."""
    interview_id = uuid.uuid4()
    await _add_turn(async_client, interview_id, "question", "Cache me")

    await async_client.get(f"/interviews/{interview_id}/turns")  # populates cache

    redis = get_redis()
    cached_raw = await redis.get(f"session:{interview_id}:turns")
    assert cached_raw is not None
    assert "Cache me" in cached_raw