from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    service_name: str = "audio-service"
    environment: str = "local"
    log_level: str = "INFO"

    # Redis DB index 2 reserved for this service's Celery broker/results —
    # see infra/docker-compose.yml.
    celery_broker_url: str = "redis://localhost:6379/2"
    celery_result_backend: str = "redis://localhost:6379/2"

    openai_api_key: str = ""

    object_storage_endpoint: str = "http://localhost:9000"
    object_storage_bucket: str = "rizzume-audio"
    object_storage_access_key: str = ""
    object_storage_secret_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
