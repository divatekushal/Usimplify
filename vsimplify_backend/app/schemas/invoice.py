from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

class InvoiceDetail(BaseModel):
    label: str
    value: str
    status: str = 'active'

class InvoiceBase(BaseModel):
    doc_id: Optional[uuid.UUID] = None
    category: Optional[str] = None
    accounting_type: Optional[str] = None
    invoice_details: Optional[List[InvoiceDetail]] = None

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(BaseModel):
    doc_id: Optional[uuid.UUID] = None
    category: Optional[str] = None
    accounting_type: Optional[str] = None
    invoice_details: Optional[List[InvoiceDetail]] = None

class InvoiceResponse(InvoiceBase):
    id: uuid.UUID
    created_date: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
