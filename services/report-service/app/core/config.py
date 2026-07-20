from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    service_name: str = "report-service"
    environment: str = "local"
    log_level: str = "INFO"

    # postgresql+asyncpg://user:password@host:port/report_db — this service's own database.
    database_url: str

    # Celery broker/result backend. Redis DB index scoped to this service —
    # see infra/docker-compose.yml for how other services get their own index.
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/1"

    # Object storage for generated PDFs (S3-compatible: MinIO locally, S3/R2 in prod).
    object_storage_endpoint: str = "http://localhost:9000"
    object_storage_bucket: str = "rizzume-reports"
    object_storage_access_key: str = ""
    object_storage_secret_key: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()
