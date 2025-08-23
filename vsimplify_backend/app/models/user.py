from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum
from app.database import Base

class UserRole(str, enum.Enum):
    OWNER = "OWNER"
    ACCOUNTANT = "ACCOUNTANT"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone_no = Column(String(20))
    location = Column(String(255))
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
