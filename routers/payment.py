import logging
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/payments", tags=["payments"])
logger = logging.getLogger(__name__)


@router.get("/")
def read_payments():
    try:
        return {"message": "Payment router working"}
    except Exception as e:
        logger.error(f"Error in read_payments: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
