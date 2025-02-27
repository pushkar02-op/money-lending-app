import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.payment import Payment
from models.loan import Loan

router = APIRouter(prefix="/payments", tags=["payments"])
logger = logging.getLogger(__name__)

@router.get("/")
def read_payments(db: Session = Depends(get_db)):
    """
    Returns a list of payments along with basic loan information.
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
