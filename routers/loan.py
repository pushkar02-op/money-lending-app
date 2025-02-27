import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.loan import Loan
from models.borrower import Borrower
from models.user import User

router = APIRouter(prefix="/loans", tags=["loans"])
logger = logging.getLogger(__name__)

@router.get("/")
def read_loans(db: Session = Depends(get_db)):
    """
    Returns a list of loans with associated borrower and agent details.
    """
    try:
        loans = db.query(Loan).all()
        result = []
        for loan in loans:
            borrower = db.query(Borrower).filter(Borrower.id == loan.borrower_id).first()
            agent = db.query(User).filter(User.id == loan.agent_id).first()
            loan_dict = {
                "id": loan.id,
                "borrower_id": loan.borrower_id,
                "borrower_name": borrower.name if borrower else None,
                "agent_id": loan.agent_id,
                "agent_name": agent.name if agent else None,
                "amount": loan.amount,
                "loan_date": loan.loan_date.isoformat() if loan.loan_date else None,
                "due_date": loan.due_date.isoformat() if loan.due_date else None,
                "status": loan.status,
            }
            result.append(loan_dict)
        return result
    except Exception as e:
        logger.error(f"Error in read_loans: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
