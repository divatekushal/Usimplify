from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

class SupplierBase(BaseModel):
    name: str
    ledger_name: Optional[str] = None
    currency_type: str = 'INR'
    gst_status: Optional[str] = None
    gst: Optional[str] = None
    address: Optional[Dict[str, Any]] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    ledger_name: Optional[str] = None
    currency_type: Optional[str] = None
    gst_status: Optional[str] = None
    gst: Optional[str] = None
    address: Optional[Dict[str, Any]] = None

class SupplierResponse(SupplierBase):
    id: uuid.UUID
    created_date: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AssignSupplierRequest(BaseModel):
    supplier_id: uuid.UUID
    company_ids: List[uuid.UUID]
