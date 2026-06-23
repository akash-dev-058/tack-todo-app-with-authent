import asyncio
import os
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base
from app.core.config import settings

# Override settings for tests
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(settings.database_url, future=True, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture()
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture()
async def client(db_session):
    async def get_test_db():
        try:
            yield db_session
        finally:
            await db_session.close()
    app.dependency_overrides["app.db.session.get_db"] = get_test_db
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac
    app.dependency_overrides.clear()
