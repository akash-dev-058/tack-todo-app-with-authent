import logging
from datetime import timedelta, datetime, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.redis_client import redis
from app.core.config import settings

logger = logging.getLogger("app.services.auth")

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def create_user(self, email: str, password: str) -> User:
        existing = await self.get_user_by_email(email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        hashed = get_password_hash(password)
        user = User(email=email, hashed_password=hashed)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        logger.info("User created: %s", email)
        return user

    async def authenticate_user(self, email: str, password: str) -> User:
        user = await self.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
        return user

    def generate_tokens(self, user: User) -> dict:
        data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def revoke_refresh_token(self, jti: str) -> None:
        # Store revoked token identifier in Redis with TTL equal to remaining expiry
        try:
            payload = decode_token(jti)  # This will raise if token invalid
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                ttl = int(exp_timestamp - datetime.now(timezone.utc).timestamp())
                await redis.setex(f"revoked:{jti}", ttl, "true")
        except Exception as exc:
            logger.error("Failed to revoke token: %s", exc)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    async def is_token_revoked(self, jti: str) -> bool:
        return await redis.exists(f"revoked:{jti}") == 1
