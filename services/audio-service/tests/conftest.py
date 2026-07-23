import os

# Safe local placeholders only — never put real credentials here, this file
# is committed. Real STT/TTS/blob calls were verified live against OpenAI
# and Azure (see current_state.md); this suite mocks them for a fast, free,
# deterministic run.
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault(
    "AZURE_CONNECTION_STRING",
    "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=dGVzdA==;EndpointSuffix=core.windows.net",
)

from unittest.mock import MagicMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_blob_upload(monkeypatch):
    upload = MagicMock(return_value="fake-blob-name")
    monkeypatch.setattr("app.api.transcriptions.blob_client.upload_blob", upload)
    return upload


@pytest.fixture
def mock_transcribe_delay(monkeypatch):
    fake_async_result = MagicMock()
    fake_async_result.id = "fake-job-id"
    delay = MagicMock(return_value=fake_async_result)
    monkeypatch.setattr("app.api.transcriptions.transcribe_audio.delay", delay)
    return delay


@pytest.fixture
def mock_celery_async_result(monkeypatch):
    """Patches the AsyncResult class used to poll job status, so tests don't
    need a real Redis broker/backend."""
    holder = {"state": "PENDING", "result": None}

    class FakeAsyncResult:
        def __init__(self, job_id, app=None):
            self.state = holder["state"]
            self.result = holder["result"]

    monkeypatch.setattr("app.api.transcriptions.AsyncResult", FakeAsyncResult)
    return holder


@pytest.fixture
def mock_tts_synthesize(monkeypatch):
    synthesize = MagicMock(return_value=b"fake-mp3-bytes")
    monkeypatch.setattr("app.api.speech.openai_tts.synthesize", synthesize)
    return synthesize
