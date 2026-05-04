from app.core.config import settings

def seed_users(db: Session):
    email = settings.DEFAULT_USER_EMAIL
    password = settings.DEFAULT_USER_PASSWORD

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return

    user = User(
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()