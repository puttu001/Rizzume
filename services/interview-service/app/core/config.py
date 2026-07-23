from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    service_name: str = "interview-service"
    environment: str = "local"
    log_level: str = "INFO"

    # postgresql+asyncpg://user:password@host:port/interview_db — this service's own database.
    database_url: str

    # Where to reach conversation-service for state/transcript writes.
    conversation_service_url: str = "http://conversation-service:8000"

    openai_api_key: str

    # Azure Blob Storage for uploaded resumes — same account as audio-service,
    # different container. Not S3-compatible, uses the azure-storage-blob SDK.
    azure_connection_string: str
    azure_resume_container_name: str = "rizzume-resumes"


@lru_cache
def get_settings() -> Settings:
    return Settings()
