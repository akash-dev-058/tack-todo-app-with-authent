import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.user import User
from app.models.todo import Todo
from app.core.security import get_password_hash
from app.core.config import settings

engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def run() -> None:
    """Create tables and populate the database with sample data.

    This script is intended for local development and testing only.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        # Create sample users
        users = []
        for i in range(1, 11):
            email = f"user{i}@example.com"
            user = User(
                email=email,
                hashed_password=get_password_hash(f"Password{i}!")
            )
            session.add(user)
            users.append(user)
        await session.commit()

        # Create todos for each user
        for user in users:
            for j in range(1, 11):
                todo = Todo(
                    user_id=user.id,
                    title=f"Todo {j} for {user.email}",
                    description="Sample todo",
                    is_completed=False,
                )
                session.add(todo)
        await session.commit()

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(run())
