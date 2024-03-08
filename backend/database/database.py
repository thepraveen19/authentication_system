# database.py
from sqlalchemy.orm import Session
from database import session

def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()
