import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import get_db
from models.user import User
from auth.security import get_password_hash, verify_password, create_access_token
from schemas.user import UserCreate, UserLogin, Token
from config import SECRET_KEY, ALGORITHM

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Optional dependency to get current user if token is provided
def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    if credentials is None:
        return None
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        user = db.query(User).filter(User.email == email).first()
        return user
    except JWTError:
        return None

# Dependency to enforce that the current user is an admin
def get_current_admin(
    current_user: Optional[User] = Depends(get_current_user_optional)
) -> User:
    if not current_user or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only an authenticated admin can register new accounts")
    return current_user

@router.post("/register", response_model=Token)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    # Check if at least one admin exists
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        # If an admin exists, require that the request comes from an authenticated admin.
        # Using get_current_admin ensures that if no valid admin token is provided,
        # an HTTPException will be raised.
        _ = get_current_admin(current_user)
    else:
        # Bootstrapping: if no admin exists, the first account must be an admin.
        if user_data.role != "admin":
            raise HTTPException(status_code=403, detail="No admin exists. The first registered account must be an admin.")

    try:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            role=user_data.role,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        access_token = create_access_token({
            "sub": new_user.email,
            "role": new_user.role,
            "user_id": new_user.id
        })
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error during registration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == user_data.email).first()
        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token({
            "sub": user.email,
            "role": user.role,
            "user_id": user.id
        })
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
