import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.core.config import settings
from app.api.v1.router import api_router
from app.middleware.logging import RequestIdMiddleware, LoggingMiddleware
from app.middleware.error_handler import http_exception_handler, validation_exception_handler
from app.middleware.auth import AuthMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
import sentry_sdk

# Initialize Sentry if DSN provided
if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=1.0,
        environment="development",
    )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AuthTodoPro API",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration – only allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middlewares
app.add_middleware(RequestIdMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(RateLimitMiddleware, max_requests=10, period_seconds=1)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Exception handlers
app.add_exception_handler(404, http_exception_handler)
app.add_exception_handler(500, http_exception_handler)
app.add_exception_handler(422, validation_exception_handler)

@app.get("/health", tags=["health"])
async def health_check(request: Request) -> JSONResponse:
    """Health check endpoint that verifies DB and Redis connectivity."""
    from app.db.session import async_engine
    from app.core.redis_client import redis
    try:
        async with async_engine.connect() as conn:
            await conn.execute("SELECT 1")
        await redis.ping()
        return JSONResponse({"status": "ok"})
    except Exception as exc:
        logger.error("Health check failed: %s", exc)
        return JSONResponse({"status": "error", "detail": str(exc)}, status_code=500)
