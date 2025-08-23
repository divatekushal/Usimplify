from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class DocumentBase(BaseModel):
    file_name: str
    file_url: str
    status: str = 'pending'
    type: Optional[str] = None
    party_name: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    file_name: Optional[str] = None
    file_url: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    party_name: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: uuid.UUID
    upload_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True
