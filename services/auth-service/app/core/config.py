from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    service_name: str = "auth-service"
    environment: str = "local"
    log_level: str = "INFO"

    # postgresql+asyncpg://user:password@host:port/auth_db — this service's own database.
    database_url: str

    # Must match JWT_SECRET/JWT_ALGORITHM in api-gateway/.env — this service issues the
    # tokens the gateway verifies.
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14


@lru_cache
def get_settings() -> Settings:
    return Settings()
