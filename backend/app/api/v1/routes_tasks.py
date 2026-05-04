from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.task import TaskCreate
from app.services import task_service

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/tasks")
def read_tasks(db: Session = Depends(get_db)):
    return task_service.get_tasks(db)

@router.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, task.title)

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service.delete_task(db, task_id)
    return {"message": "deleted"}