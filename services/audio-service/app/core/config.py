from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    service_name: str = "audio-service"
    environment: str = "local"
    log_level: str = "INFO"

    # Numbered Redis DBs (the original /2 plan) don't work against a hosted
    # instance — confirmed live against Upstash: "Only 0th database is
    # supported!". Isolation from other services' Celery traffic instead
    # comes from a distinct queue name (see worker/celery_app.py's
    # task_default_queue), not the DB index. docker-compose.yml's local
    # Redis still gets a distinct index for clarity there, but the queue
    # name is what actually matters here.
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"

    openai_api_key: str

    # Azure Blob Storage — not S3-compatible, uses the azure-storage-blob
    # SDK. See current_state.md for why Azure over an S3-compatible service.
    azure_connection_string: str
    azure_container_name: str = "rizzume-audio"


@lru_cache
def get_settings() -> Settings:
    return Settings()
