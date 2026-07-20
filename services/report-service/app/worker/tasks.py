from app.worker.celery_app import celery_app


@celery_app.task(name="report.ping")
def ping() -> str:
    """Proves the worker boots and can reach the broker. Replace/extend with
    the real generate_report task once app/generators/ has actual logic."""
    return "pong"
