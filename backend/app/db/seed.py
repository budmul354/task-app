from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password

def seed_users(db: Session):
    existing = db.query(User).filter(User.email == "admin@example.com").first()

    if existing:
        print("✅ Default user already exists")
        return

    user = User(
        email="admin@example.com",
        hashed_password=hash_password("admin123")
    )

    db.add(user)
    db.commit()

    print("🚀 Default user created: admin@example.com / admin123")