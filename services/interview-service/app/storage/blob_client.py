from functools import lru_cache

from azure.storage.blob import ContainerClient, ContentSettings

from app.core.config import get_settings


@lru_cache
def get_container_client() -> ContainerClient:
    settings = get_settings()
    return ContainerClient.from_connection_string(
        settings.azure_connection_string, container_name=settings.azure_resume_container_name
    )


def upload_resume(blob_name: str, data: bytes) -> str:
    """Returns the blob name — access happens through this service, not a
    public URL (the container isn't public)."""
    container = get_container_client()
    container.upload_blob(
        name=blob_name,
        data=data,
        overwrite=True,
        content_settings=ContentSettings(content_type="application/pdf"),
    )
    return blob_name