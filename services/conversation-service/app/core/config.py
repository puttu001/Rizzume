from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    service_name: str = "conversation-service"
    environment: str = "local"
    log_level: str = "INFO"

    # postgresql+asyncpg://user:password@host:port/conversation_db — the durable transcript store.
    database_url: str

    # Active-session cache — this is the Redis box in architecture.png, DB index
    # scoped to this service only (see infra/docker-compose.yml).
    redis_url: str = "redis://localhost:6379/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
