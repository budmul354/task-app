from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.task import TaskCreate, TaskResponse
from app.services import task_service

router = APIRouter()


@router.get("/tasks", response_model=list[TaskResponse])
def read_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return task_service.get_tasks(db, user.id)


@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return task_service.create_task(db, task.title, user.id)
