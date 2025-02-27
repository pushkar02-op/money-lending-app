import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from auth.security import get_current_user, require_role

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)

@router.get("/")
def read_users(db: Session = Depends(get_db)):
    """
    Returns a list of all users.
    """
    try:
        users = db.query(User).all()
        result = []
        for user in users:
            user_dict = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
            }
            result.append(user_dict)
        return result
    except Exception as e:
        logger.error(f"Error in read_users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/admin-dashboard", summary="Admin Dashboard")
def admin_dashboard(user: User = Depends(require_role("admin"))):
    """
    Endpoint accessible only by admin users.
    You can later extend this to return aggregated data.
    """
    return {"message": f"Welcome {user.name}, you are an admin."}

@router.get("/agent-dashboard", summary="Agent Dashboard")
def agent_dashboard(user: User = Depends(require_role("agent"))):
    """
    Endpoint accessible only by agent users.
    """
    return {"message": f"Welcome {user.name}, you are an agent."}
