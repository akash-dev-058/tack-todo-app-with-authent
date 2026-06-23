# AuthTodoPro Backend

A production‑ready FastAPI backend for the AuthTodoPro application.

## Features
- Async PostgreSQL with SQLAlchemy 2.x
- JWT authentication (access + refresh) stored in HttpOnly cookies
- Redis‑backed rate limiting and token blacklisting
- Server‑Sent Events for real‑time todo updates
- Structured logging, Sentry integration, health checks
- Alembic migrations and seed script
- Comprehensive pytest suite

## Quick Start
bash
# Clone repository
git clone <repo-url>
cd backend

# Create .env from example and edit values
cp .env.example .env

# Build and run containers
docker compose up --build -d

# Apply migrations
docker compose exec backend make migrate

# Run tests
docker compose exec backend make test


The API docs are available at `http://localhost:8000/docs`.

## Environment Variables
See `.env.example` for a full list.

## Testing
Run `make test` inside the container or locally (requires a running PostgreSQL and Redis).

## License
MIT