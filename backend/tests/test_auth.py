import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_register_and_login(client: AsyncClient):
    # Register
    resp = await client.post("/api/v1/auth/register", json={"email": "test@example.com", "password": "StrongPass123"})
    assert resp.status_code == status.HTTP_201_CREATED
    assert "access_token" in resp.json()
    # Login
    resp = await client.post("/api/v1/auth/login", json={"email": "test@example.com", "password": "StrongPass123"})
    assert resp.status_code == status.HTTP_200_OK
    assert "access_token" in resp.json()

@pytest.mark.asyncio
async def test_invalid_login(client: AsyncClient):
    resp = await client.post("/api/v1/auth/login", json={"email": "nonexistent@example.com", "password": "nopass"})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
