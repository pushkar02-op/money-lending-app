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
