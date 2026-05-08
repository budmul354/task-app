from sqlalchemy.orm import Session
from app.models.task import Task

def get_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.owner_id == user_id).all()

def create_task(db: Session, title: str, user_id: int):
    task = Task(title=title, owner_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task