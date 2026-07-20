from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    service_name: str = "api-gateway"
    environment: str = "local"
    log_level: str = "INFO"

    jwt_secret: str
    jwt_algorithm: str = "HS256"

    cors_allowed_origins: list[str] = ["http://localhost:3000"]

    auth_service_url: str = "http://auth-service:8000"
    interview_service_url: str = "http://interview-service:8000"
    audio_service_url: str = "http://audio-service:8000"
    report_service_url: str = "http://report-service:8000"


@lru_cache
def get_settings() -> Settings:
    return Settings()
