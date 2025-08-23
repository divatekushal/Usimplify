from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.auth import verify_token

security = HTTPBearer()

def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token.credentials)
    if username is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == username).first()
    if user is None:
        raise credentials_exception
    return user

def require_owner(current_user: User = Depends(get_current_user)):
    if current_user.role != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only owners can access this resource"
        )
    return current_user
