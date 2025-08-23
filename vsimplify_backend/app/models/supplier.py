from sqlalchemy import Column, String, DateTime, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

# Association table for company-supplier relationship
company_supplier_relation = Table(
    'company_supplier_relation',
    Base.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('company_id', UUID(as_uuid=True), ForeignKey('company.id', ondelete='CASCADE')),
    Column('supplier_id', UUID(as_uuid=True), ForeignKey('supplier.id', ondelete='CASCADE')),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

class Supplier(Base):
    __tablename__ = "supplier"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    ledger_name = Column(String(255))
    currency_type = Column(String(10), default='INR')
    gst_status = Column(String(20))
    gst = Column(String(50))
    address = Column(JSONB)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    companies = relationship("Company", secondary=company_supplier_relation)
