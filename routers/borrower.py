import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.borrower import Borrower
from models.user import User

router = APIRouter(prefix="/borrowers", tags=["borrowers"])
logger = logging.getLogger(__name__)

@router.get("/")
def read_borrowers(db: Session = Depends(get_db)):
    """
    Returns a list of borrowers with their assigned agent details.
    """
    try:
        borrowers = db.query(Borrower).all()
        result = []
        for borrower in borrowers:
            agent = db.query(User).filter(User.id == borrower.assigned_agent_id).first()
            borrower_dict = {
                "id": borrower.id,
                "name": borrower.name,
                "contact_info": borrower.contact_info,
                "assigned_agent_id": borrower.assigned_agent_id,
                "assigned_agent_name": agent.name if agent else None,
            }
            result.append(borrower_dict)
        return result
    except Exception as e:
        logger.error(f"Error in read_borrowers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
