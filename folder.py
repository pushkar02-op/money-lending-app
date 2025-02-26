# Project: Money Lending App
# Stack: React (Frontend) + Python (Backend) + MySQL (Database)
# Backend Framework: FastAPI (for performance & async support)
# Security: JWT Authentication, Input Validation, Role-Based Access Control (RBAC)

# Directory Structure
# money_lending_app/
# ├── main.py
# ├── config.py
# ├── database.py
# ├── models/
# │   ├── base.py
# │   ├── user.py
# │   ├── borrower.py
# │   ├── loan.py
# │   ├── payment.py
# ├── schemas/
# │   ├── user.py
# │   ├── borrower.py
# │   ├── loan.py
# │   ├── payment.py
# ├── crud/
# │   ├── user.py
# │   ├── borrower.py
# │   ├── loan.py
# │   ├── payment.py
# ├── auth/
# │   ├── security.py
# │   ├── jwt.py
# ├── dependencies.py
# ├── routers/
# │   ├── user.py
# │   ├── borrower.py
# │   ├── loan.py
# │   ├── payment.py
# ├── requirements.txt

# config.py
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "mysql+pymysql://root:password@localhost/money_lending"

# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

gine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# models/base.py
from database import Base

# models/user.py
from sqlalchemy import Column, Integer, String, Enum
from models.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum("admin", "agent", name="user_roles"), default="agent")

# models/borrower.py
from sqlalchemy import Column, Integer, String, ForeignKey
from models.base import Base

class Borrower(Base):
    __tablename__ = "borrowers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact_info = Column(String)
    assigned_agent_id = Column(Integer, ForeignKey("users.id"))

# models/loan.py
from sqlalchemy import Column, Integer, Float, Date, ForeignKey, Enum
from datetime import datetime
from models.base import Base

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"))
    agent_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    loan_date = Column(Date, default=datetime.utcnow)
    due_date = Column(Date, nullable=False)
    status = Column(Enum("active", "completed", name="loan_status"), default="active")

# models/payment.py
from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from datetime import datetime
from models.base import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"))
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(Date, default=datetime.utcnow)

# auth/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# auth/jwt.py
from datetime import datetime, timedelta
from jose import jwt
from config import SECRET_KEY, ALGORITHM

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# dependencies.py
from database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# main.py
from fastapi import FastAPI
from database import Base, engine
import models.user, models.borrower, models.loan, models.payment
from routers import user, borrower, loan, payment

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(borrower.router)
app.include_router(loan.router)
app.include_router(payment.router)

# requirements.txt
fastapi
uvicorn
sqlalchemy
pymysql
python-jose
bcrypt
