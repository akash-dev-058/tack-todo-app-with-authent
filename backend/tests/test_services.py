import pytest
from app.services.auth_service import AuthService
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_password_hashing():
    pwd = "Secret123!"
    hashed = get_password_hash(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed)

@pytest.mark.asyncio
async def test_token_generation(db_session: AsyncSession):
    service = AuthService(db_session)
    user = User(email="svc@example.com", hashed_password=get_password_hash("Pass1234"))
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    tokens = service.generate_tokens(user)
    assert "access_token" in tokens and "refresh_token" in tokens
