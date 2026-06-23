from fastapi import Depends, Request, HTTPException, status
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    # Optionally, fetch fresh user from DB to ensure existence
    from app.models.user import User
    result = await db.execute(select(User).where(User.id == user["id"]))
    db_user = result.scalars().first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return db_user
