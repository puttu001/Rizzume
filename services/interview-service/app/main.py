from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging()

app = FastAPI(title=settings.service_name)


# Registered before include_router deliberately — see the comment on this
# same pattern in auth-service/app/main.py. This is the service where the
# bug actually bit: `/{interview_id}` (untyped) matched "/health" before the
# `:uuid` converter fix, and even with that fix this ordering is still the
# right defense-in-depth default.
@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_name}


app.include_router(api_router)
