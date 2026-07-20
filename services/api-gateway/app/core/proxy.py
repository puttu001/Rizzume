import httpx
from fastapi import Request, Response

# Headers that are hop-by-hop or connection-specific and must not be replayed
# from the downstream response onto the response we send back to the client.
_STRIPPED_RESPONSE_HEADERS = {"content-encoding", "transfer-encoding", "connection"}


async def proxy_request(request: Request, client: httpx.AsyncClient, downstream_path: str) -> Response:
    """Forward the incoming request to a downstream service, attaching the
    authenticated user id (set by JWTAuthMiddleware) as a trusted header."""
    headers = dict(request.headers)
    headers.pop("host", None)

    user_id = getattr(request.state, "user_id", None)
    if user_id is not None:
        headers["x-user-id"] = str(user_id)

    body = await request.body()
    downstream_response = await client.request(
        request.method,
        downstream_path,
        params=request.query_params,
        headers=headers,
        content=body,
    )

    return Response(
        content=downstream_response.content,
        status_code=downstream_response.status_code,
        headers={
            key: value
            for key, value in downstream_response.headers.items()
            if key.lower() not in _STRIPPED_RESPONSE_HEADERS
        },
    )
