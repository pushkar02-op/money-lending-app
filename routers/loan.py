import logging
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/loans", tags=["loans"])
logger = logging.getLogger(__name__)


@router.get("/")
def read_loans():
    try:
        return {"message": "Loan router working"}
    except Exception as e:
        logger.error(f"Error in read_loans: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
