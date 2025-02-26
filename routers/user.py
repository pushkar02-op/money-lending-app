import logging
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)

@router.get("/")
def read_users():
    try:
        return {"message": "User router working"}
    except Exception as e:
        logger.error(f"Error in read_users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
