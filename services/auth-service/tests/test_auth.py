import uuid

import jwt
from httpx import AsyncClient


async def _signup(client: AsyncClient, email: str, password: str = "correcthorsebattery"):
    return await client.post("/signup", json={"email": email, "password": password})


def access_token_subject(token: str) -> str:
    return jwt.decode(token, options={"verify_signature": False})["sub"]


async def test_signup_returns_tokens(async_client, clean_users_table) -> None:
    response = await _signup(async_client, f"{uuid.uuid4()}@example.com")
    assert response.status_code == 201
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["refresh_token"]


async def test_signup_duplicate_email_is_conflict(async_client, clean_users_table) -> None:
    email = f"{uuid.uuid4()}@example.com"
    assert (await _signup(async_client, email)).status_code == 201
    assert (await _signup(async_client, email)).status_code == 409


async def test_login_wrong_password_is_unauthorized(async_client, clean_users_table) -> None:
    email = f"{uuid.uuid4()}@example.com"
    await _signup(async_client, email)
    response = await async_client.post("/login", json={"email": email, "password": "wrong"})
    assert response.status_code == 401


async def test_login_correct_password_returns_tokens(async_client, clean_users_table) -> None:
    email = f"{uuid.uuid4()}@example.com"
    await _signup(async_client, email, password="correcthorsebattery")
    response = await async_client.post(
        "/login", json={"email": email, "password": "correcthorsebattery"}
    )
    assert response.status_code == 200
    assert response.json()["access_token"]


async def test_me_requires_x_user_id_header(async_client, clean_users_table) -> None:
    response = await async_client.get("/me")
    assert response.status_code == 401


async def test_me_returns_the_signed_up_user(async_client, clean_users_table) -> None:
    email = f"{uuid.uuid4()}@example.com"
    signup_response = await _signup(async_client, email)
    user_id = access_token_subject(signup_response.json()["access_token"])

    response = await async_client.get("/me", headers={"X-User-Id": user_id})
    assert response.status_code == 200
    assert response.json()["email"] == email


async def test_refresh_with_refresh_token_returns_new_tokens(
    async_client, clean_users_table
) -> None:
    email = f"{uuid.uuid4()}@example.com"
    signup_response = await _signup(async_client, email)
    refresh_token = signup_response.json()["refresh_token"]

    response = await async_client.post("/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert response.json()["access_token"]


async def test_refresh_rejects_an_access_token(async_client, clean_users_table) -> None:
    email = f"{uuid.uuid4()}@example.com"
    signup_response = await _signup(async_client, email)
    access_token = signup_response.json()["access_token"]

    response = await async_client.post("/refresh", json={"refresh_token": access_token})
    assert response.status_code == 401