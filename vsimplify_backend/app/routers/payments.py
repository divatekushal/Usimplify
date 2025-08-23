from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.models.payment import PostingPaymentDetails
from app.models.user import User
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentUpdate
from app.utils.dependencies import get_current_user
import uuid

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=PaymentResponse)
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_payment = PostingPaymentDetails(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@router.get("/", response_model=List[PaymentResponse])
def get_payments(
    skip: int = 0,
    limit: int = 100,
    payment_mode: Optional[str] = None,
    payment_source: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(PostingPaymentDetails)
    
    if payment_mode:
        query = query.filter(PostingPaymentDetails.payment_mode == payment_mode)
    if payment_source:
        query = query.filter(PostingPaymentDetails.payment_source == payment_source)
    if start_date:
        query = query.filter(PostingPaymentDetails.posting_date >= start_date)
    if end_date:
        query = query.filter(PostingPaymentDetails.posting_date <= end_date)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = db.query(PostingPaymentDetails).filter(PostingPaymentDetails.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment

@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: uuid.UUID,
    payment_update: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = db.query(PostingPaymentDetails).filter(PostingPaymentDetails.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    for field, value in payment_update.dict(exclude_unset=True).items():
        setattr(payment, field, value)
    
    db.commit()
    db.refresh(payment)
    return payment

@router.delete("/{payment_id}")
def delete_payment(
    payment_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = db.query(PostingPaymentDetails).filter(PostingPaymentDetails.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    db.delete(payment)
    db.commit()
    return {"message": "Payment deleted successfully"}

@router.get("/ref/{ref_no}", response_model=PaymentResponse)
def get_payment_by_ref(
    ref_no: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payment = db.query(PostingPaymentDetails).filter(PostingPaymentDetails.ref_no == ref_no).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found with this reference number"
        )
    return payment

@router.get("/date-range/{start_date}/{end_date}", response_model=List[PaymentResponse])
def get_payments_by_date_range(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    payments = db.query(PostingPaymentDetails).filter(
        PostingPaymentDetails.posting_date >= start_date,
        PostingPaymentDetails.posting_date <= end_date
    ).all()
    return payments

@router.get("/summary/total")
def get_payment_summary(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    payment_mode: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from sqlalchemy import func
    
    query = db.query(
        func.count(PostingPaymentDetails.id).label('total_payments'),
        func.sum(PostingPaymentDetails.amount_paid).label('total_amount_paid'),
        func.sum(PostingPaymentDetails.total_amount).label('total_amount')
    )
    
    if start_date:
        query = query.filter(PostingPaymentDetails.posting_date >= start_date)
    if end_date:
        query = query.filter(PostingPaymentDetails.posting_date <= end_date)
    if payment_mode:
        query = query.filter(PostingPaymentDetails.payment_mode == payment_mode)
    
    result = query.first()
    
    return {
        "total_payments": result.total_payments or 0,
        "total_amount_paid": float(result.total_amount_paid) if result.total_amount_paid else 0.0,
        "total_amount": float(result.total_amount) if result.total_amount else 0.0
    }
