from functools import lru_cache

from azure.storage.blob import ContainerClient, ContentSettings

from app.core.config import get_settings


@lru_cache
def get_container_client() -> ContainerClient:
    settings = get_settings()
    return ContainerClient.from_connection_string(
        settings.azure_connection_string, container_name=settings.azure_container_name
    )


def upload_blob(blob_name: str, data: bytes, *, content_type: str = "audio/webm") -> str:
    """Returns the blob name — access happens through this service, not a
    public URL (the container isn't public)."""
    container = get_container_client()
    container.upload_blob(
        name=blob_name,
        data=data,
        overwrite=True,
        content_settings=ContentSettings(content_type=content_type),
    )
    return blob_name


def download_blob(blob_name: str) -> bytes:
    container = get_container_client()
    return container.download_blob(blob_name).readall()