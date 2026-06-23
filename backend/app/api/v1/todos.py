import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.todo import TodoCreate, TodoRead, TodoUpdate
from app.services.todo_service import TodoService
from app.api.deps import get_current_user, get_db

router = APIRouter()
logger = logging.getLogger("app.api.v1.todos")

@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_in: TodoCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TodoService(db, user_id=current_user.id)
    todo = await service.create_todo(title=todo_in.title, description=todo_in.description)
    return todo

@router.get("/", response_model=List[TodoRead])
async def list_todos(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TodoService(db, user_id=current_user.id)
    todos = await service.list_todos(skip=skip, limit=limit)
    return todos

@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(
    todo_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TodoService(db, user_id=current_user.id)
    todo = await service.get_todo(todo_id)
    return todo

@router.put("/{todo_id}", response_model=TodoRead)
async def update_todo(
    todo_id: int,
    todo_in: TodoUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TodoService(db, user_id=current_user.id)
    todo = await service.update_todo(todo_id, **todo_in.dict(exclude_unset=True))
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = TodoService(db, user_id=current_user.id)
    await service.delete_todo(todo_id)
    return None
