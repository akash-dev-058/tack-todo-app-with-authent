import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.fixture
async def auth_headers(client: AsyncClient):
    """Register a user and log in, returning the client with cookies set.
    The fixture returns an empty dict because the ``AsyncClient`` instance
    automatically stores cookies received from the server.
    """
    # Register the user
    await client.post(
        "/api/v1/auth/register",
        json={"email": "todo_user@example.com", "password": "TodoPass123"},
    )
    # Log in to obtain HttpOnly cookies
    resp = await client.post(
        "/api/v1/auth/login",
        json={"email": "todo_user@example.com", "password": "TodoPass123"},
    )
    assert resp.status_code == status.HTTP_200_OK
    return {}

@pytest.mark.asyncio
async def test_create_and_get_todo(client: AsyncClient, auth_headers):
    # Create a todo
    resp = await client.post(
        "/api/v1/todos/",
        json={"title": "Test Todo", "description": "Details"},
    )
    assert resp.status_code == status.HTTP_201_CREATED
    todo = resp.json()
    todo_id = todo["id"]

    # Retrieve the same todo
    resp = await client.get(f"/api/v1/todos/{todo_id}")
    assert resp.status_code == status.HTTP_200_OK
    fetched = resp.json()
    assert fetched["title"] == "Test Todo"

@pytest.mark.asyncio
async def test_todo_isolation(client: AsyncClient):
    # User A registers and creates a todo
    await client.post(
        "/api/v1/auth/register",
        json={"email": "usera@example.com", "password": "Pass12345"},
    )
    await client.post(
        "/api/v1/auth/login",
        json={"email": "usera@example.com", "password": "Pass12345"},
    )
    resp = await client.post(
        "/api/v1/todos/",
        json={"title": "User A Todo"},
    )
    todo_a_id = resp.json()["id"]

    # Logout User A (simple endpoint that clears cookies)
    await client.post("/api/v1/auth/logout")

    # User B registers and logs in
    await client.post(
        "/api/v1/auth/register",
        json={"email": "userb@example.com", "password": "Pass12345"},
    )
    await client.post(
        "/api/v1/auth/login",
        json={"email": "userb@example.com", "password": "Pass12345"},
    )

    # Attempt to access User A's todo – should be 404
    resp = await client.get(f"/api/v1/todos/{todo_a_id}")
    assert resp.status_code == status.HTTP_404_NOT_FOUND
