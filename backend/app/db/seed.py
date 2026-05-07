from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User


def seed_users(db: Session) -> User:
    email = settings.DEFAULT_USER_EMAIL
    password = settings.DEFAULT_USER_PASSWORD

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return existing

    user = User(
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
