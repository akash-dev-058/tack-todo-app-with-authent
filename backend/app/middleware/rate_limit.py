import time
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis_client import redis
from app.core.config import settings
import logging

logger = logging.getLogger("app.middleware.rate_limit")

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple token bucket rate limiter using Redis.

    Limits requests per IP per period as defined in settings.
    """
    def __init__(self, app, max_requests: int = None, period_seconds: int = None):
        super().__init__(app)
        self.max_requests = max_requests or settings.rate_limit_max_requests
        self.period = period_seconds or settings.rate_limit_period_seconds

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rl:{client_ip}"
        try:
            current = await redis.get(key)
            if current is None:
                await redis.set(key, 1, ex=self.period)
            elif int(current) < self.max_requests:
                await redis.incr(key)
            else:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded",
                )
        except Exception as exc:
            logger.error("Rate limiting error: %s", exc)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Rate limiting failure")
        response = await call_next(request)
        return response
