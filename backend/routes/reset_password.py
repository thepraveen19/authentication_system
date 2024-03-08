import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from services.auth_service import send_password_reset_email
from database.models import PasswordResetToken, User
from config.config import SECRET_KEY, ALGORITHM
from configparser import ConfigParser
from database.database import get_db
from routes.schemas import PasswordResetRequest

EMAIL_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "email.ini")
config = ConfigParser()
config.read(EMAIL_CONFIG_PATH)
domain = config["Credentials"]["domain"]

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define a function to generate a secure token for password reset
def generate_password_reset_token(email: str):
    # Define the payload for the JWT token
    token_payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Token expiration time (e.g., 1 hour)
        "iat": datetime.utcnow(),  # Token issue time
        "type": "password-reset",  # Custom type to identify the purpose of the token
    }

    # Encode the token using the provided secret key and algorithm
    token = jwt.encode(token_payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def store_reset_token(email: str, reset_token: str, expiration_minutes: int = 60):
    # Fetch the user from the database based on the provided email
    db = session.SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        # Handle the case where the user is not found
        db.close()
        raise Exception("User not found")

    expiration_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    
    # Create a new PasswordResetToken record
    db_token = PasswordResetToken(user_id=user.user_id, token=reset_token, expiration_time=expiration_time)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    db.close()

    return db_token

@router.post("/forgot-password", response_model=dict)
def forgot_password(request_data: PasswordResetRequest, db: Session = Depends(get_db)):
    # Extract email from the request data
    email = request_data.email

    # Check if the user exists
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate a secure token for password reset
    reset_token = generate_password_reset_token(email)

    reset_link = f"https://{domain}/reset-password?token={reset_token}"

    # Implemented logic to securely store the reset_token temporarily (e.g., in the database)
    store_reset_token(email=email, reset_token=reset_token)

    # Send a password reset email using the auth_service
    send_password_reset_email(email, reset_link)

    # Return a message indicating that instructions have been sent
    return {"message": "Password reset instructions sent to the provided email"}

# rest password
def verify_password_reset_token(token: str) -> User:
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extract the email from the payload
        email = payload.get("sub")

        # Retrieve the user from the database based on the email
        db = session.SessionLocal()
        user = db.query(User).filter(User.email == email).first()

        # Retrieve the corresponding password reset token
        reset_token = (
            db.query(PasswordResetToken)
            .filter(
                PasswordResetToken.user_id == user.user_id,
                PasswordResetToken.token == token,
                PasswordResetToken.is_used == False,  # Check if the token is not marked as used
                PasswordResetToken.expiration_time >= datetime.utcnow(),  # Check if the token is not expired
            )
            .first()
        )

        db.close()

        if reset_token:
            return user

    except JWTError:
        # Handle JWT errors, for example, token expired or invalid signature
        pass

    return None


def invalidate_reset_token(token_id: str):
    # Retrieve the token from the database based on the token_id (assuming it's a JWT token)
    db = session.SessionLocal()
    token = db.query(PasswordResetToken).filter(PasswordResetToken.token == token_id).first()

    # Check if the token exists
    if token:
        # Mark the token as used or invalid (update the database)
        token.is_used = True
        token.used_at = datetime.utcnow()  # Record the timestamp when the token was used
        db.commit()

    db.close()

@router.get("/reset-password", response_model=dict)
# @router.post("/reset-password", response_model=dict)
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    # Verify the token (you need to implement this logic)
    user = verify_password_reset_token(token)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Update the user's password
    hashed_password = pwd_context.hash(new_password)
    user.hashed_password = hashed_password
    db.commit()

    # Optionally, invalidate or delete the used token from the temporary storage
    invalidate_reset_token(token)

    return {"message": "Password reset successfully"}