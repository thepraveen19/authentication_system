import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import models
from passlib.context import CryptContext
from database.database import get_db
from routes.schemas import UserRegistration

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=dict)
def register_user(user_data: UserRegistration, db: Session = Depends(get_db)):
    # Check if the email is already registered
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email is already registered")

    # Hash the password (use a suitable hashing library like bcrypt)
    hashed_password = pwd_context.hash(user_data.password)

    # Create a new user in the database
    new_user = models.User(
        email=user_data.email,
        hashed_password=hashed_password,
        phone_number=user_data.phone_number,
        role_id=1
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}