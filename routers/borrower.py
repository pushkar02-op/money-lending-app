import logging
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/borrowers", tags=["borrowers"])
logger = logging.getLogger(__name__)

@router.get("/")
def read_borrowers():
    try:
        return {"message": "Borrower router working"}
    except Exception as e:
        logger.error(f"Error in read_borrowers: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
