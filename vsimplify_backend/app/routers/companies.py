from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.company import Company, company_user_relation
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate, AssignAccountantRequest
from app.utils.dependencies import get_current_user, require_owner
import uuid

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=CompanyResponse)
def create_company(
    company: CompanyCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(require_owner)
):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.get("/", response_model=List[CompanyResponse])
def get_companies(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "owner":
        return db.query(Company).all()
    else:
        # Return only companies assigned to this accountant
        return db.query(Company).join(company_user_relation).filter(
            company_user_relation.c.user_id == current_user.id
        ).all()

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: uuid.UUID, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    return company

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: uuid.UUID,
    company_update: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    for field, value in company_update.dict(exclude_unset=True).items():
        setattr(company, field, value)
    
    db.commit()
    db.refresh(company)
    return company

@router.delete("/{company_id}")
def delete_company(
    company_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner)
):
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    db.delete(company)
    db.commit()
    return {"message": "Company deleted successfully"}

@router.post("/assign-accountant")
def assign_accountant_to_companies(
    request: AssignAccountantRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_owner)
):
    # Verify accountant exists
    accountant = db.query(User).filter(
        User.id == request.user_id, 
        User.role == "accountant"
    ).first()
    if not accountant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Accountant not found"
        )
    
    # Remove existing assignments
    db.execute(
        company_user_relation.delete().where(
            company_user_relation.c.user_id == request.user_id
        )
    )
    
    # Add new assignments
    for company_id in request.company_ids:
        db.execute(
            company_user_relation.insert().values(
                company_id=company_id,
                user_id=request.user_id
            )
        )
    
    db.commit()
    return {"message": "Accountant assigned to companies successfully"}
