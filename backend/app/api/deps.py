from fastapi import Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.config import settings

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
    except:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.email == email).first()
    return user