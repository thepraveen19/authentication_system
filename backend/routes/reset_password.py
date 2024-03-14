import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from services.auth_service import send_password_reset_email
from database.models import PasswordResetToken, User, PasswordResetKey
from database.database import get_db
from routes.schemas import PasswordResetRequest
import secrets, string


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_reset_token(email: str, user_id: int, db: Session) -> PasswordResetToken:
    # Construct a UTC datetime from time.time()
    utc_now = datetime.utcnow()

    # Calculate expiration time (e.g., 1 hour from now)
    expiration_time = utc_now + timedelta(hours=1)

    # Generate a unique random token
    token_characters = string.ascii_letters + string.digits
    reset_token = ''.join(secrets.choice(token_characters) for i in range(32))  # Generate a 32-character token

    # Create a new PasswordResetToken object with the user_id provided
    reset_token_obj = PasswordResetToken(
        user_id=user_id,
        token=reset_token,
        expiration_time=expiration_time,
        issued=utc_now,
        is_used=False,
        used_at=None
    )

    # Commit the token to the database
    db.add(reset_token_obj)
    db.commit()

    return reset_token_obj


def store_reset_token(email: str, reset_token: str, expiration_minutes: int = 60):
    db = session.SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    db_token = PasswordResetToken(user_id=user.id, token=reset_token, expiration_time=expiration_time)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    db.close()
    return db_token


def generate_unique_key(length: int = 6) -> str:
    return secrets.token_urlsafe(length)


def associate_key_with_token(db: Session, reset_key: str, reset_token_id: int, user_id: int):
    db_key = PasswordResetKey(key=reset_key, reset_token_id=reset_token_id, user_id=user_id)
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key



@router.post("/forgot-password", response_model=dict)
def forgot_password(request_data: PasswordResetRequest, db: Session = Depends(get_db)):
    email = request_data.email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset_token = generate_password_reset_token(email, user.user_id, db)  # Change user.id to user.user_id
    print(reset_token.id)

    reset_key = generate_unique_key()
    print(reset_key)
    
    associate_key_with_token(db, reset_key, reset_token.id,user.user_id )

    reset_link = f"{reset_key}"

    send_password_reset_email(email, reset_link)

    return {"message": "Password reset instructions sent to the provided email"}

def verify_password_reset_key(key: str, db: Session):
    reset_key = db.query(PasswordResetKey).filter(PasswordResetKey.key == key).first()
    if not reset_key:
        return None, None
    
    reset_token_id = reset_key.reset_token_id
    reset_token = db.query(PasswordResetToken).filter(PasswordResetToken.id == reset_token_id).first()
    
    if not reset_token or reset_token.is_used or reset_token.expiration_time < datetime.utcnow():
        return None, None
    
    return reset_token, reset_key.user_id

def invalidate_reset_key(key: str, db: Session):
    reset_key = db.query(PasswordResetKey).filter(PasswordResetKey.key == key).first()
    if reset_key:
        db.delete(reset_key)
        db.commit()

@router.post("/reset-password", response_model=dict)
def reset_password(key: str, new_password: str, db: Session = Depends(get_db)):
    # Verify the password reset key and retrieve the associated reset token
    reset_token, user_id = verify_password_reset_key(key, db)

    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired key")

    # Retrieve the associated reset key object
    reset_key = db.query(PasswordResetKey).filter(PasswordResetKey.key == key).first()

    if not reset_key:
        raise HTTPException(status_code=404, detail="Reset key not found")

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Hash the new password
    hashed_password = pwd_context.hash(new_password)

    # Update the user's password in the database
    user.hashed_password = hashed_password
  
    # Invalidate the password reset key
    invalidate_reset_key(key, db)
    reset_token.is_used = True
    reset_token.used_at = datetime.utcnow()
    db.commit()

    return {"message": "Password reset successfully"}




