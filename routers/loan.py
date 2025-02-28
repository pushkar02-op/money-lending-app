"""
Loan API Routes:

- `GET /loans/`: Fetch all loans with computed remaining balance and associated names.
- `GET /loans/{loan_id}/details`: Fetch a specific loan with computed remaining balance.
- `GET /loans/summary`: Aggregates total outstanding loans per agent (by name).
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, datetime
from sqlalchemy import func
from database import get_db
from models.loan import Loan
from models.payment import Payment
from models.user import User
from models.borrower import Borrower
from schemas.loan import LoanOut
from services.loanService import get_remaining_balance
from auth.security import require_role
from schemas.loan import LoanIssue


router = APIRouter(prefix="/loans", tags=["loans"])

@router.get("/", response_model=list[LoanOut])
def read_loans(db: Session = Depends(get_db)):
    """
    Fetch all loans along with computed remaining balance and associated names.
    
    :param db: Database session.
    :return: List of loans with computed remaining balance and names.
    """
    loans = db.query(Loan).all()
    loan_data = []
    for loan in loans:
        # Get agent name from User table
        agent = db.query(User).filter(User.id == loan.agent_id).first()
        agent_name = agent.name if agent else None

        # Get borrower name from Borrower table
        borrower = db.query(Borrower).filter(Borrower.id == loan.borrower_id).first()
        borrower_name = borrower.name if borrower else None

        loan_info = {**loan.__dict__, "remaining_balance": get_remaining_balance(loan.id, db)}
        loan_info["agent_name"] = agent_name
        loan_info["borrower_name"] = borrower_name
        loan_data.append(loan_info)
    return loan_data

@router.get("/{loan_id}/details")
def get_loan_details(loan_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single loan along with computed remaining balance and associated names.
    
    :param loan_id: Loan ID.
    :param db: Database session.
    :return: Loan details including computed remaining balance and names.
    """
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    agent = db.query(User).filter(User.id == loan.agent_id).first()
    agent_name = agent.name if agent else None

    borrower = db.query(Borrower).filter(Borrower.id == loan.borrower_id).first()
    borrower_name = borrower.name if borrower else None

    return {**loan.__dict__,
            "remaining_balance": get_remaining_balance(loan.id, db),
            "agent_name": agent_name,
            "borrower_name": borrower_name}

@router.get("/summary")
def loan_summary(db: Session = Depends(get_db)):
    """
    Aggregates total outstanding loans per agent.
    For each agent, calculates the sum of remaining balances for all active loans.
    
    :param db: Database session.
    :return: List of dictionaries with agent's name and total outstanding balance.
    """
    try:
        loans = db.query(Loan).filter(Loan.status == "active").all()
        summary = {}
        for loan in loans:
            rem_balance = get_remaining_balance(loan.id, db)
            # Fetch agent name
            agent = db.query(User).filter(User.id == loan.agent_id).first()
            agent_name = agent.name if agent else "Unknown"
            if agent_name in summary:
                summary[agent_name] += rem_balance
            else:
                summary[agent_name] = rem_balance
        result = [
            {"agent_name": agent_name, "total_outstanding": round(total, 2)}
            for agent_name, total in summary.items()
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {e}")
    
@router.post("/issue", dependencies=[Depends(require_role("agent"))])
def issue_loan(
    loan_data: LoanIssue,
    db: Session = Depends(get_db),
    agent_user: User = Depends(require_role("agent"))  # ensures only agents can call this endpoint
):
    """
    Creates a new borrower (if not already existing) and issues a new loan.
    This endpoint is restricted to agents.
    
    :param loan_data: LoanIssue schema containing borrower and loan details.
    :param db: Database session.
    :param agent_user: The agent making the request (validated by role).
    :return: Newly created loan details.
    """
    # Ensure the agent_id in payload matches the authenticated agent's id
    if loan_data.agent_id != agent_user.id:
        raise HTTPException(status_code=403, detail="Cannot issue loan on behalf of another agent.")

    # Check if the borrower exists (by name) and create if not
    existing_borrower = db.query(Borrower).filter(Borrower.name == loan_data.borrower_name).first()
    if not existing_borrower:
        new_borrower = Borrower(
            name=loan_data.borrower_name,
            contact_info=loan_data.borrower_contact,
            assigned_agent_id=loan_data.agent_id
        )
        db.add(new_borrower)
        db.commit()
        db.refresh(new_borrower)
        borrower_id = new_borrower.id
    else:
        borrower_id = existing_borrower.id

    # Create the new loan using the provided data
    new_loan = Loan(
        borrower_id=borrower_id,
        agent_id=loan_data.agent_id,
        amount=loan_data.amount,
        interest_rate=loan_data.interest_rate,
        repayment_method=loan_data.repayment_method,
        payment_frequency=loan_data.payment_frequency,
        loan_date=datetime.utcnow(),  # you can also accept a loan_date if needed
        status="active"
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return {
        "message": "Loan issued successfully",
        "loan_id": new_loan.id,
        "borrower_id": new_loan.borrower_id,
        "agent_id": new_loan.agent_id,
        "amount": new_loan.amount,
        "interest_rate": new_loan.interest_rate,
        "repayment_method": new_loan.repayment_method,
        "payment_frequency": new_loan.payment_frequency,
        "status": new_loan.status
    }