from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid

class CompanyBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    location: Optional[Dict[str, Any]] = None
    base_currency: str = 'INR'
    gst_number: Optional[str] = None
    accounting_month: Optional[int] = None
    contact_person: Optional[Dict[str, Any]] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    location: Optional[Dict[str, Any]] = None
    base_currency: Optional[str] = None
    gst_number: Optional[str] = None
    accounting_month: Optional[int] = None
    contact_person: Optional[Dict[str, Any]] = None

class CompanyResponse(CompanyBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class AssignAccountantRequest(BaseModel):
    user_id: uuid.UUID
    company_ids: List[uuid.UUID]
