import logging
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.todo import Todo

logger = logging.getLogger("app.repositories.todo")

class TodoRepository:
    """Data‑access layer for Todo entities.

    All methods are async and use SQLAlchemy Core expressions.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id_and_user(self, todo_id: int, user_id: int) -> Optional[Todo]:
        result = await self.db.execute(
            select(Todo)
            .where(Todo.id == todo_id, Todo.user_id == user_id)
            .options(selectinload(Todo.owner))
        )
        return result.scalars().first()

    async def list_by_user(self, user_id: int, skip: int = 0, limit: int = 20) -> List[Todo]:
        result = await self.db.execute(
            select(Todo)
            .where(Todo.user_id == user_id)
            .order_by(Todo.created_at.desc())
            .offset(skip)
            .limit(limit)
            .options(selectinload(Todo.owner))
        )
        return result.scalars().all()

    async def create(self, todo: Todo) -> Todo:
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)
        logger.info("Created todo %s for user %s", todo.id, todo.user_id)
        return todo

    async def update(self, todo: Todo) -> Todo:
        await self.db.commit()
        await self.db.refresh(todo)
        logger.info("Updated todo %s", todo.id)
        return todo

    async def delete(self, todo: Todo) -> None:
        await self.db.delete(todo)
        await self.db.commit()
        logger.info("Deleted todo %s", todo.id)
