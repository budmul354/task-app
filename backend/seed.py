from app.db.session import SessionLocal
from app.db.base import Base
from app.db.session import engine
from app.db.seed import seed_users

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = seed_users(db)
        print(f"Seeded user: {user.email}")
    finally:
        db.close()

if __name__ == "__main__":
    run()
