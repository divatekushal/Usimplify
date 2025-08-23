from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal
import uuid

class PaymentBase(BaseModel):
    posting_date: Optional[date] = None
    booking_remarks: Optional[str] = None
    date_of_payment: Optional[date] = None
    payment_mode: Optional[str] = None
    payment_source: Optional[str] = None
    amount_paid: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    ref_no: Optional[str] = None
    narration: Optional[str] = None
    doc_of_proof_url: Optional[str] = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    posting_date: Optional[date] = None
    booking_remarks: Optional[str] = None
    date_of_payment: Optional[date] = None
    payment_mode: Optional[str] = None
    payment_source: Optional[str] = None
    amount_paid: Optional[Decimal] = None
    total_amount: Optional[Decimal] = None
    ref_no: Optional[str] = None
    narration: Optional[str] = None
    doc_of_proof_url: Optional[str] = None

class PaymentResponse(PaymentBase):
    id: uuid.UUID
    created_date: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
