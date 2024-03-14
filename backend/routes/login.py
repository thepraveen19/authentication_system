# routes/authentication.py
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import models
from jose import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from config.config import SECRET_KEY, ALGORITHM
from configparser import ConfigParser
from database.database import get_db
from routes.schemas import UserLogin

EMAIL_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "email.ini")
config = ConfigParser()
config.read(EMAIL_CONFIG_PATH)
domain = config["Credentials"]["domain"]

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to create a JWT token
def create_jwt_token(user_id: int, expires_delta: timedelta):
    to_encode = {"sub": str(user_id), "exp": datetime.utcnow() + expires_delta}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login", response_model=dict)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        # Check if the user exists
        user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate JWT token
        access_token_expires = timedelta(minutes=30)
        access_token = create_jwt_token(user_id=user.user_id, expires_delta=access_token_expires)

        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Login error: {e}")
        raise

