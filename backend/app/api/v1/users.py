import logging
from fastapi import APIRouter, Depends, status
from app.schemas.user import UserRead
from app.api.deps import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
logger = logging.getLogger("app.api.v1.users")

@router.get("/me", response_model=UserRead, status_code=status.HTTP_200_OK)
async def read_current_user(current_user = Depends(get_current_user)):
    return current_user
