from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .todos import router as todos_router
from .events import router as events_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(todos_router, prefix="/todos", tags=["todos"])
api_router.include_router(events_router, prefix="/events", tags=["events"])
