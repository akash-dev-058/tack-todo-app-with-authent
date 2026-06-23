from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import decode_token
from app.core.redis_client import redis
from app.core.config import settings
import logging

logger = logging.getLogger("app.middleware.auth")

class AuthMiddleware(BaseHTTPMiddleware):
    """Extract JWT from HttpOnly cookie, validate, and attach user info to request.state."""
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("access_token")
        if token:
            try:
                payload = decode_token(token)
                if payload.get("type") != "access":
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
                request.state.user = {
                    "id": int(payload.get("sub")),
                    "email": payload.get("email"),
                }
            except Exception as exc:
                logger.warning("Auth token validation failed: %s", exc)
                request.state.user = None
        else:
            request.state.user = None
        response = await call_next(request)
        return response
