"""
Loan Model: Defines the structure of the loans table.

- `id`: Unique identifier for each loan.
- `borrower_id`: References the borrower.
- `agent_id`: References the agent managing the loan.
- `amount`: Total loan amount.
- `loan_date`: Date when the loan was issued.
- `interest_rate`: Monthly interest rate (decimal format, e.g., 0.02 for 2%).
- `repayment_method`: Either 'full' (one-time repayment) or 'interest' (recurring payments).
- `payment_frequency`: If repayment is 'interest', specifies 'daily' or 'monthly'.
- `status`: Current status of the loan ('active' or 'completed').
"""

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
    interest_rate = Column(Float, nullable=False)
    repayment_method = Column(Enum("full", "interest", name="loan_repayment_method"), default="full")
    payment_frequency = Column(Enum("daily", "monthly", name="payment_frequency"), nullable=True)
    status = Column(Enum("active", "completed", name="loan_status"), default="active")
