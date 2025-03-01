import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import get_db
from models.user import User
from models.borrower import Borrower
from models.loan import Loan
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

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    transfer_agent_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    """
    Deletes an agent with the given ID.
    If the agent has borrowers or loans assigned, you can optionally provide a transfer_agent_id
    to reassign those references (in borrowers and loans tables) to another agent before deletion.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != "agent":
        raise HTTPException(status_code=400, detail="Can only delete agent users")
    
    if transfer_agent_id is not None:
        if transfer_agent_id == user_id:
            raise HTTPException(
                status_code=400, 
                detail="Transfer agent cannot be the same as the agent to delete"
            )
        new_agent = db.query(User).filter(User.id == transfer_agent_id).first()
        if not new_agent or new_agent.role != "agent":
            raise HTTPException(
                status_code=400, 
                detail="Invalid transfer agent provided"
            )
        # Transfer all borrowers assigned to this agent
        db.query(Borrower).filter(Borrower.assigned_agent_id == user_id).update(
            {"assigned_agent_id": transfer_agent_id}
        )
        # Transfer all loans created by this agent
        db.query(Loan).filter(Loan.agent_id == user_id).update(
            {"agent_id": transfer_agent_id}
        )
        db.commit()
    else:
        # If no transfer agent is provided, check if there are any references in borrowers or loans
        borrower_count = db.query(Borrower).filter(Borrower.assigned_agent_id == user_id).count()
        loan_count = db.query(Loan).filter(Loan.agent_id == user_id).count()
        if borrower_count > 0 or loan_count > 0:
            raise HTTPException(
                status_code=400,
                detail="Agent has borrowers or loans assigned. Provide transfer_agent_id to transfer them before deletion."
            )
    
    try:
        db.delete(user)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Failed to delete agent due to a foreign key constraint."
        )
    return {"message": "Agent deleted successfully"}