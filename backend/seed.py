from app.db.session import SessionLocal
from app.db.seed import seed_users

def run():
    db = SessionLocal()
    try:
        seed_users(db)
    finally:
        db.close()

if __name__ == "__main__":
    run()