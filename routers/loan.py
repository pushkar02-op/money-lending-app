# routers/loan.py
"""
Loan API Routes:

- GET /loans/ : Fetch paginated & filtered loans with computed remaining balance and associated names.
- GET /loans/{loan_id}/details : Fetch a specific loan with computed remaining balance.
- GET /loans/summary : Aggregates total outstanding loans per agent.
- GET /loans/metrics : Returns global key metrics (total loans, total amount lent, active & completed loans).
- POST /loans/issue : Issue a new loan (restricted to agents).
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from sqlalchemy import func
from database import get_db
from models.loan import Loan
from models.user import User
from models.borrower import Borrower
from schemas.loan import LoanOut, LoanIssue
from services.loanService import get_remaining_balance
from auth.security import require_role

router = APIRouter(prefix="/loans", tags=["loans"])

@router.get("/", response_model=list[LoanOut])
def read_loans(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, description="Maximum number of records to return"),
    status: str = Query(None, description="Filter by loan status (active/completed)"),
    agent_id: int = Query(None, description="Filter by agent ID"),
    borrower_id: int = Query(None, description="Filter by borrower ID"),
    sort_by: str = Query("loan_date", description="Sort by field (loan_date or amount)"),
    order: str = Query("desc", description="Sort order (asc or desc)")
):
    query = db.query(Loan)
    if status:
        query = query.filter(Loan.status == status)
    if agent_id:
        query = query.filter(Loan.agent_id == agent_id)
    if borrower_id:
        query = query.filter(Loan.borrower_id == borrower_id)
    
    # Allow sorting only by safe columns
    allowed_sort = {"loan_date": Loan.loan_date, "amount": Loan.amount}
    if sort_by in allowed_sort:
        sort_column = allowed_sort[sort_by]
        if order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    
    loans = query.offset(skip).limit(limit).all()
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
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    agent = db.query(User).filter(User.id == loan.agent_id).first()
    agent_name = agent.name if agent else None

    borrower = db.query(Borrower).filter(Borrower.id == loan.borrower_id).first()
    borrower_name = borrower.name if borrower else None

    return {
        **loan.__dict__,
        "remaining_balance": get_remaining_balance(loan.id, db),
        "agent_name": agent_name,
        "borrower_name": borrower_name
    }

@router.get("/summary")
def loan_summary(db: Session = Depends(get_db)):
    try:
        loans = db.query(Loan).filter(Loan.status == "active").all()
        summary = {}
        for loan in loans:
            rem_balance = get_remaining_balance(loan.id, db)
            agent = db.query(User).filter(User.id == loan.agent_id).first()
            agent_name = agent.name if agent else "Unknown"
            summary[agent_name] = summary.get(agent_name, 0) + rem_balance
        result = [
            {"agent_name": agent_name, "total_outstanding": round(total, 2)}
            for agent_name, total in summary.items()
        ]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {e}")

@router.get("/metrics")
def loan_metrics(db: Session = Depends(get_db)):
    """
    Returns key metrics including total loans, total amount lent,
    active loans count, and completed loans count.
    """
    try:
        total_loans = db.query(func.count(Loan.id)).scalar()
        total_amount_lent = db.query(func.coalesce(func.sum(Loan.amount), 0)).scalar()
        active_loans = db.query(func.count(Loan.id)).filter(Loan.status == "active").scalar()
        completed_loans = db.query(func.count(Loan.id)).filter(Loan.status == "completed").scalar()
        return {
            "total_loans": total_loans,
            "total_amount_lent": round(total_amount_lent, 2),
            "active_loans": active_loans,
            "completed_loans": completed_loans
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating metrics: {e}")
    
@router.post("/issue", dependencies=[Depends(require_role("agent"))])
def issue_loan(
    loan_data: LoanIssue,
    db: Session = Depends(get_db),
    agent_user: User = Depends(require_role("agent"))
):
    if loan_data.agent_id != agent_user.id:
        raise HTTPException(status_code=403, detail="Cannot issue loan on behalf of another agent.")

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

    new_loan = Loan(
        borrower_id=borrower_id,
        agent_id=loan_data.agent_id,
        amount=loan_data.amount,
        interest_rate=loan_data.interest_rate,
        repayment_method=loan_data.repayment_method,
        payment_frequency=loan_data.payment_frequency,
        loan_date=loan_data.loan_date if loan_data.loan_date else datetime.utcnow(),
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
