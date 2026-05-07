# Task App

## Backend Setup

Create a local backend environment file from the example:

```powershell
Copy-Item backend\.env.example backend\.env
```

Update `SECRET_KEY` before deploying anywhere public.

This project is configured for PostgreSQL on port `5434` with user `budim`:

```text
postgresql+psycopg2://budim@localhost:5434/task_app
```

Install dependencies, seed the default user, and run the API:

```powershell
cd backend
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe seed.py
.\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The API accepts JSON login at `POST /login` and Bearer-token auth for `/tasks`.
