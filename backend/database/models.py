from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base, relationship
import os
import sys
from database.session import engine

Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    phone_number = Column(String, nullable=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), default=1)  # Default role is a regular user

    # Additional fields
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    full_name = Column(String, nullable=True)
    avatar = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    password_reset_token = Column(String, nullable=True)
    role = relationship("Role", back_populates="users")

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    token = Column(String, unique=True, index=True)
    expiration_time = Column(DateTime, nullable=False)
    issued = Column(DateTime, default=datetime.utcnow)  # New field to store the issuance time
    is_used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)

# Add a relationship between the tables
User.reset_tokens = relationship("PasswordResetToken", back_populates="user")
PasswordResetToken.user = relationship("User", back_populates="reset_tokens")
Role.users = relationship("User", back_populates="role")

# Create the tables
Base.metadata.create_all(engine)
