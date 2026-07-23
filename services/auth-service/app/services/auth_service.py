from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories import user_repository
from app.schemas.user import TokenResponse
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


def _issue_tokens(user: User) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


async def signup(db: AsyncSession, *, email: str, password: str) -> TokenResponse:
    if await user_repository.get_by_email(db, email) is not None:
        raise EmailAlreadyRegisteredError(email)

    user = await user_repository.create(db, email=email, hashed_password=hash_password(password))
    await db.commit()
    return _issue_tokens(user)


async def login(db: AsyncSession, *, email: str, password: str) -> TokenResponse:
    user = await user_repository.get_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        raise InvalidCredentialsError()
    return _issue_tokens(user)


async def refresh(db: AsyncSession, *, refresh_token: str) -> TokenResponse:
    user_id = decode_token(refresh_token, expected_type="refresh")
    user = await user_repository.get_by_id(db, user_id)
    if user is None:
        raise InvalidCredentialsError()
    return _issue_tokens(user)