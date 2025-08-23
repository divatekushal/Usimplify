from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoice"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id = Column(UUID(as_uuid=True), ForeignKey('document.id', ondelete='SET NULL'))
    category = Column(String(100))
    accounting_type = Column(String(100))
    invoice_details = Column(JSONB)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    document = relationship("Document", back_populates="invoices")
