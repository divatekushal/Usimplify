from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class Document(Base):
    __tablename__ = "document"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String(255), nullable=False)
    file_url = Column(Text, nullable=False)
    status = Column(String(50), default='pending')
    type = Column(String(100))
    party_name = Column(String(255))
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    invoices = relationship("Invoice", back_populates="document")
