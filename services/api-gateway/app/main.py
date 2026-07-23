from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.clients.registry import close_clients
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.middleware.auth import JWTAuthMiddleware

settings = get_settings()
configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_clients()


app = FastAPI(title=settings.service_name, lifespan=lifespan)

# Order matters: Starlette makes the LAST-added middleware outermost, so
# CORS must be added after JWT — otherwise JWT's early 401 responses never
# pass through CORS and browsers show a CORS error instead of the real 401.
app.add_middleware(JWTAuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Registered before include_router deliberately — see the comment on this
# same pattern in auth-service/app/main.py. Not actually at risk here since
# every gateway route is prefixed (/api/v1/...), but keeping the ordering
# consistent across all six services beats relying on "this one's fine."
@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.service_name}


app.include_router(api_router)
