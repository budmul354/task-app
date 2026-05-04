from fastapi import FastAPI
from app.api.v1.routes_tasks import router as task_router
from app.api.v1.routes_auth import router as auth_router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(task_router)