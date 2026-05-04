from fastapi import FastAPI
from backend.app.api.v1.routes_tasks import router as task_router
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(task_router)