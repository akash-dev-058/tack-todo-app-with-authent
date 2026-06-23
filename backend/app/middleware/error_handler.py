import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

logger = logging.getLogger("app.middleware.error_handler")

async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error("HTTPException: %s - %s", exc.status_code, exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

async def validation_exception_handler(request: Request, exc):
    # FastAPI's RequestValidationError
    logger.error("Validation error: %s", exc.errors())
    return JSONResponse(status_code=422, content={"detail": exc.errors()})
