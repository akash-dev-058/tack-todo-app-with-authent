import logging
import uuid
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("app.middleware.logging")

class RequestIdMiddleware(BaseHTTPMiddleware):
    """Assign a unique request ID to each incoming request for traceability."""
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

class LoggingMiddleware(BaseHTTPMiddleware):
    """Log request method, path, status code, and duration with request ID."""
    async def dispatch(self, request, call_next):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.info("%s %s - start", request.method, request.url.path, extra={"request_id": request_id})
        try:
            response = await call_next(request)
            return response
        finally:
            logger.info(
                "%s %s - %s", request.method, request.url.path, getattr(response, "status_code", "-"),
                extra={"request_id": request_id},
            )
