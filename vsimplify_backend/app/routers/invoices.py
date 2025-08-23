from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.invoice import Invoice
from app.models.document import Document
from app.models.user import User
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceUpdate
from app.utils.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.post("/", response_model=InvoiceResponse)
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify document exists if doc_id is provided
    if invoice.doc_id:
        document = db.query(Document).filter(Document.id == invoice.doc_id).first()
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
    
    # Convert invoice_details to JSON format
    invoice_details_json = None
    if invoice.invoice_details:
        invoice_details_json = [detail.dict() for detail in invoice.invoice_details]
    
    db_invoice = Invoice(
        doc_id=invoice.doc_id,
        category=invoice.category,
        accounting_type=invoice.accounting_type,
        invoice_details=invoice_details_json
    )
    
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

@router.get("/", response_model=List[InvoiceResponse])
def get_invoices(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    accounting_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Invoice)
    
    if category:
        query = query.filter(Invoice.category == category)
    if accounting_type:
        query = query.filter(Invoice.accounting_type == accounting_type)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    return invoice

@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
    invoice_id: uuid.UUID,
    invoice_update: InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    # Handle invoice_details conversion
    update_data = invoice_update.dict(exclude_unset=True)
    if 'invoice_details' in update_data and update_data['invoice_details']:
        update_data['invoice_details'] = [detail.dict() for detail in update_data['invoice_details']]
    
    for field, value in update_data.items():
        setattr(invoice, field, value)
    
    db.commit()
    db.refresh(invoice)
    return invoice

@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invoice not found"
        )
    
    db.delete(invoice)
    db.commit()
    return {"message": "Invoice deleted successfully"}

@router.get("/document/{document_id}", response_model=List[InvoiceResponse])
def get_invoices_by_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoices = db.query(Invoice).filter(Invoice.doc_id == document_id).all()
    return invoices

@router.get("/category/{category}", response_model=List[InvoiceResponse])
def get_invoices_by_category(
    category: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    invoices = db.query(Invoice).filter(Invoice.category == category).all()
    return invoices
