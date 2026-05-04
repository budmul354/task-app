from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    status = Column(String, default="todo")
    owner_id = Column(Integer, ForeignKey("users.id"))