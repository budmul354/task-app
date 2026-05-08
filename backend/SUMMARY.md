# Backend Summary

This folder contains the FastAPI backend for Task App. It provides authentication, user-scoped task endpoints, database access, and local deployment configuration.

## What It Does

- Starts a FastAPI app from `app/main.py`.
- Creates database tables on application startup with SQLAlchemy metadata.
- Exposes JSON login at `POST /login`.
- Issues bearer JWT access tokens after successful login.
- Protects task routes with bearer-token authentication.
- Stores users and tasks in PostgreSQL through SQLAlchemy models.
- Seeds a default user through `seed.py`.

## Main API

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| `POST` | `/login` | No | Accepts email and password, then returns an access token. |
| `GET` | `/tasks` | Yes | Returns tasks owned by the current authenticated user. |
| `POST` | `/tasks` | Yes | Creates a new task for the current authenticated user. |

## Key Files

- `app/main.py` configures the FastAPI app, CORS, startup table creation, and routers.
- `app/api/v1/routes_auth.py` handles login.
- `app/api/v1/routes_task.py` handles task listing and creation.
- `app/api/v1/routes_tasks.py` re-exports the task router used by `main.py`.
- `app/api/deps.py` provides database sessions and resolves the current user from JWTs.
- `app/core/config.py` loads environment-backed settings.
- `app/core/security.py` hashes passwords, verifies passwords, and creates JWTs.
- `app/models/` defines the `User` and `Task` database tables.
- `app/schemas/` defines Pydantic request and response shapes.
- `app/services/task_service.py` contains task database operations.
- `app/db/seed.py` creates the configured default user if it does not already exist.
- `seed.py` creates tables and runs the seed routine.

## Data Model

`users`

- `id`
- `email`
- `hashed_password`

`tasks`

- `id`
- `title`
- `status`
- `owner_id`

Each task belongs to a user through `owner_id`, and task queries are filtered by the authenticated user's id.

## Configuration

Settings are loaded from `.env` and `.env.local` by `pydantic-settings`.
Values in `.env.local` override matching values from `.env`.

Important values:

- `DATABASE_URL`
- `SECRET_KEY`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `ALLOWED_ORIGINS`
- `DEFAULT_USER_EMAIL`
- `DEFAULT_USER_PASSWORD`

The default database URL points to PostgreSQL on port `5434`:

```text
postgresql+psycopg2://budim@localhost:5434/task_app
```

## Running Locally

```powershell
cd backend
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe seed.py
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The backend can also be built with the included `Dockerfile`. The `docker-compose.yml` exposes the API on port `8000` and points the container at the host PostgreSQL database.
