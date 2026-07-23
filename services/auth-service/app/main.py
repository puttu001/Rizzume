from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging()

app = FastAPI(title=settings.service_name)


# Registered before include_router deliberately: an untyped path parameter
# in a mounted router (e.g. `/{some_id}`) can otherwise shadow a literal
# path like `/health` if it's added first — Starlette matches routes in
# registration order, and "health" is valid input for an untyped
# string path converter. See interview-service's `/{interview_id:uuid}` fix
# for the same issue caught there.
@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_name}


app.include_router(api_router)
