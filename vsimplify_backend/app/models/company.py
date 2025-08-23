from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

# Association table for many-to-many relationship
company_user_relation = Table(
    'company_user_relation',
    Base.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('company_id', UUID(as_uuid=True), ForeignKey('company.id', ondelete='CASCADE')),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

class Company(Base):
    __tablename__ = "company"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255))
    location = Column(JSONB)
    base_currency = Column(String(10), default='INR')
    gst_number = Column(String(50))
    accounting_month = Column(Integer)
    contact_person = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    users = relationship("User", secondary=company_user_relation, back_populates="companies")

# Add to User model
from app.models.user import User
User.companies = relationship("Company", secondary=company_user_relation, back_populates="users")
