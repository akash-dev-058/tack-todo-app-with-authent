import logging
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.todo import Todo
from app.repositories.todo_repository import TodoRepository

logger = logging.getLogger("app.services.todo")

class TodoService:
    """Business‑logic layer for Todo operations.

    All methods enforce that the current user can only interact with
    their own Todo records.
    """

    def __init__(self, db: AsyncSession, user_id: int):
        self.db = db
        self.user_id = user_id
        self.repo = TodoRepository(db)

    async def get_todo(self, todo_id: int) -> Todo:
        """Retrieve a single Todo belonging to the current user.

        Raises
        ------
        HTTPException
            404 if the Todo does not exist or does not belong to the user.
        """
        todo = await self.repo.get_by_id_and_user(todo_id, self.user_id)
        if not todo:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return todo

    async def list_todos(self, skip: int = 0, limit: int = 20) -> List[Todo]:
        """Return a paginated list of Todos for the current user.

        The ``limit`` is capped at 100 to protect against abuse.
        """
        if limit > 100:
            limit = 100
        return await self.repo.list_by_user(self.user_id, skip=skip, limit=limit)

    async def create_todo(self, title: str, description: Optional[str] = None) -> Todo:
        """Create a new Todo for the current user."""
        todo = Todo(user_id=self.user_id, title=title, description=description)
        await self.repo.create(todo)
        return todo

    async def update_todo(self, todo_id: int, **kwargs) -> Todo:
        """Update fields of an existing Todo.

        ``kwargs`` may contain any of the mutable fields defined in
        :class:`app.schemas.todo.TodoUpdate`.
        """
        todo = await self.get_todo(todo_id)
        for key, value in kwargs.items():
            if hasattr(todo, key) and value is not None:
                setattr(todo, key, value)
        await self.repo.update(todo)
        return todo

    async def delete_todo(self, todo_id: int) -> None:
        """Delete a Todo belonging to the current user."""
        todo = await self.get_todo(todo_id)
        await self.repo.delete(todo)
