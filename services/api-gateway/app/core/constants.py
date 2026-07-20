# Paths the JWT auth middleware lets through without a bearer token.
PUBLIC_PATHS: set[str] = {
    "/health",
    "/api/v1/auth/signup",
    "/api/v1/auth/login",
    "/api/v1/auth/refresh",
}
