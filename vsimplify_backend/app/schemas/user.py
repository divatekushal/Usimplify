from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

class UserRole(str, Enum):
    OWNER = "OWNER"
    ACCOUNTANT = "ACCOUNTANT"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone_no: Optional[str] = None
    location: Optional[str] = None
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_no: Optional[str] = None
    location: Optional[str] = None

class UserResponse(UserBase):
    id: uuid.UUID
    created_date: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
