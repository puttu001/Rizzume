import ssl

from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "audio_service",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.worker.tasks"],
)

# rediss:// (TLS, what Upstash requires) needs explicit cert verification
# config or Celery refuses to start at all — confirmed live:
# "A rediss:// URL must have parameter ssl_cert_reqs...". Plain redis-py
# (used directly in conversation-service) didn't need this; Celery's kombu
# transport does.
_redis_tls_opts = {"ssl_cert_reqs": ssl.CERT_REQUIRED}

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_track_started=True,
    # Distinct queue name is the real isolation from report-service's worker
    # sharing this same Redis instance — numbered DBs don't work against a
    # hosted instance (confirmed live: Upstash only supports DB 0), so
    # without this both workers would consume from the same default
    # "celery" queue and steal each other's tasks.
    task_default_queue="audio_tasks",
    broker_use_ssl=_redis_tls_opts if settings.celery_broker_url.startswith("rediss://") else None,
    redis_backend_use_ssl=(
        _redis_tls_opts if settings.celery_result_backend.startswith("rediss://") else None
    ),
)
