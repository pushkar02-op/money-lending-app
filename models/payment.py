from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from datetime import datetime
from models.base import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"))
    amount_paid = Column(Float, nullable=False)
    payment_date = Column(Date, default=datetime.utcnow)
