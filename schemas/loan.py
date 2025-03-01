# schemas/loan.py
from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

class LoanRepaymentMethod(str, Enum):
    full = "full"
    interest = "interest"

class PaymentFrequency(str, Enum):
    daily = "daily"
    monthly = "monthly"

class LoanOut(BaseModel):
    id: int
    borrower_id: int
    agent_id: int
    amount: float
    loan_date: date
    interest_rate: float
    repayment_method: LoanRepaymentMethod
    payment_frequency: Optional[PaymentFrequency] = None
    status: str
    remaining_balance: float
    agent_name: Optional[str] = None
    borrower_name: Optional[str] = None

    class Config:
        from_attributes = True

class LoanIssue(BaseModel):
    borrower_name: str
    borrower_contact: Optional[str] = None
    amount: float
    interest_rate: float
    repayment_method: LoanRepaymentMethod
    payment_frequency: Optional[PaymentFrequency] = None
    agent_id: int  # The agent issuing the loan
    loan_date: Optional[date] = None  # New optional field for loan date
