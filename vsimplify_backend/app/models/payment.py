from sqlalchemy import Column, String, DateTime, DECIMAL, Date, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base

class PostingPaymentDetails(Base):
    __tablename__ = "posting_payment_details"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    posting_date = Column(Date)
    booking_remarks = Column(Text)
    date_of_payment = Column(Date)
    payment_mode = Column(String(50))
    payment_source = Column(String(100))
    amount_paid = Column(DECIMAL(15, 2))
    total_amount = Column(DECIMAL(15, 2))
    ref_no = Column(String(100))
    narration = Column(Text)
    doc_of_proof_url = Column(Text)
    created_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
