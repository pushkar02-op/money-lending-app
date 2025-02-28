"""
Payment API Routes:

- `GET /payments/`: Fetch all payments with loan details.
- `POST /payments/pay`: Allows an agent to record a payment.
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.payment import Payment
from models.loan import Loan
from services.loanService import get_remaining_balance
from schemas.payment import PaymentCreate  # Import the schema


router = APIRouter(prefix="/payments", tags=["payments"])
logger = logging.getLogger(__name__)

@router.get("/")
def read_payments(db: Session = Depends(get_db)):
    """
    Returns a list of payments along with basic loan information.
    
    :param db: Database session.
    :return: List of recorded payments.
    """
    try:
        payments = db.query(Payment).all()
        result = []
        for payment in payments:
            loan = db.query(Loan).filter(Loan.id == payment.loan_id).first()
            payment_dict = {
                "id": payment.id,
                "loan_id": payment.loan_id,
                "amount_paid": payment.amount_paid,
                "payment_date": payment.payment_date.isoformat() if payment.payment_date else None,
                "loan_amount": loan.amount if loan else None,
            }
            result.append(payment_dict)
        return result
    except Exception as e:
        logger.error(f"Error in read_payments: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post("/pay")
def record_payment(payment_data: PaymentCreate, db: Session = Depends(get_db)):
    """
    Records a payment for a given loan.

    :param payment_data: Payment details (loan_id, amount_paid).
    :param db: Database session.
    :return: Success message with updated remaining balance.
    """
    loan = db.query(Loan).filter(Loan.id == payment_data.loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    remaining_balance = get_remaining_balance(loan.id, db)

    if remaining_balance is None:
        raise HTTPException(status_code=500, detail="Error calculating remaining balance.")

    if remaining_balance <= 0:
        raise HTTPException(status_code=400, detail="Loan is already fully repaid.")

    if payment_data.amount_paid > remaining_balance:
        raise HTTPException(status_code=400, detail="Payment exceeds remaining balance.")

    new_payment = Payment(loan_id=payment_data.loan_id, amount_paid=payment_data.amount_paid)
    db.add(new_payment)
    db.commit()

    updated_balance = get_remaining_balance(loan.id, db)  # Ensure it's re-fetched after update

    return {
    "message": "Payment recorded successfully",
    "remaining_balance": round(updated_balance, 2)  # Ensure response is rounded
}
