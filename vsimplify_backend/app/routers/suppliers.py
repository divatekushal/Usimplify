from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.supplier import Supplier, company_supplier_relation
from app.models.company import Company
from app.models.user import User
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate, AssignSupplierRequest
from app.utils.dependencies import get_current_user, require_owner
import uuid

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

@router.post("/", response_model=SupplierResponse)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_supplier = Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(
    skip: int = 0,
    limit: int = 100,
    currency_type: Optional[str] = None,
    gst_status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Supplier)
    
    if currency_type:
        query = query.filter(Supplier.currency_type == currency_type)
    if gst_status:
        query = query.filter(Supplier.gst_status == gst_status)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    return supplier

@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: uuid.UUID,
    supplier_update: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    for field, value in supplier_update.dict(exclude_unset=True).items():
        setattr(supplier, field, value)
    
    db.commit()
    db.refresh(supplier)
    return supplier

@router.delete("/{supplier_id}")
def delete_supplier(
    supplier_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    db.delete(supplier)
    db.commit()
    return {"message": "Supplier deleted successfully"}

@router.post("/assign-to-companies")
def assign_supplier_to_companies(
    request: AssignSupplierRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner)
):
    # Verify supplier exists
    supplier = db.query(Supplier).filter(Supplier.id == request.supplier_id).first()
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier not found"
        )
    
    # Verify all companies exist
    for company_id in request.company_ids:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company with id {company_id} not found"
            )
    
    # Remove existing assignments for this supplier
    db.execute(
        company_supplier_relation.delete().where(
            company_supplier_relation.c.supplier_id == request.supplier_id
        )
    )
    
    # Add new assignments
    for company_id in request.company_ids:
        db.execute(
            company_supplier_relation.insert().values(
                company_id=company_id,
                supplier_id=request.supplier_id
            )
        )
    
    db.commit()
    return {"message": "Supplier assigned to companies successfully"}

@router.get("/company/{company_id}", response_model=List[SupplierResponse])
def get_suppliers_by_company(
    company_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify company exists and user has access
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    suppliers = db.query(Supplier).join(company_supplier_relation).filter(
        company_supplier_relation.c.company_id == company_id
    ).all()
    
    return suppliers

@router.delete("/company/{company_id}/supplier/{supplier_id}")
def remove_supplier_from_company(
    company_id: uuid.UUID,
    supplier_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner)
):
    # Remove the specific company-supplier relationship
    result = db.execute(
        company_supplier_relation.delete().where(
            (company_supplier_relation.c.company_id == company_id) &
            (company_supplier_relation.c.supplier_id == supplier_id)
        )
    )
    
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplier-Company relationship not found"
        )
    
    db.commit()
    return {"message": "Supplier removed from company successfully"}
