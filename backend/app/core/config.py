from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Core settings
    backend_url: str = "http://localhost:8000"
    frontend_url: str = "http://localhost:3000"

    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/auth_todo_db"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret_key: str = "CHANGE_ME_TO_A_STRONG_RANDOM_VALUE"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Security
    rate_limit_max_requests: int = 10
    rate_limit_period_seconds: int = 1

    # Optional integrations
    sentry_dsn: str | None = None
    resend_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
