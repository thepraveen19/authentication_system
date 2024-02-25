from pydantic import BaseModel, EmailStr  
# Updated Pydantic model for user registration data
class UserRegistration(BaseModel):
    email: EmailStr  # Use EmailStr instead of str for email
    password: str
    phone_number: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Define a Pydantic model for the request data
class PasswordResetRequest(BaseModel):
    email: EmailStr