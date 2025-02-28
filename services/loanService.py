"""
Loan Service: Contains utility functions to handle loan calculations.

- `calculate_full_repayment_amount()`: Computes the total amount due for full-repayment loans.
- `calculate_interest_due()`: Computes the interest accrued over a given period.
- `get_remaining_balance()`: Dynamically computes the outstanding loan balance including simple interest.
"""

from datetime import date
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from models.loan import Loan
from models.payment import Payment

def calculate_full_repayment_amount(loan: Loan, as_of_date: date = None) -> float:
    """
    Calculates the total repayment amount for 'full' loans, including interest accrued.
    
    :param loan: Loan instance.
    :param as_of_date: Date for which to calculate the total due amount (default: today).
    :return: Total repayment amount including interest.
    """
    if as_of_date is None:
        as_of_date = date.today()
    
    days_elapsed = (as_of_date - loan.loan_date).days
    months_elapsed = days_elapsed / 30  # Approximate conversion
    # Convert percentage interest to decimal by dividing by 100
    total_due = loan.amount * (1 + (loan.interest_rate / 100) * months_elapsed)
    return total_due

def calculate_interest_due(loan: Loan, start_date: date, end_date: date) -> float:
    """
    Calculates the interest due for 'interest' loans over a given period.
    
    :param loan: Loan instance.
    :param start_date: Start date of the interest calculation period.
    :param end_date: End date of the interest calculation period.
    :return: Interest amount due for the given period.
    """
    days_elapsed = (end_date - start_date).days

    if loan.payment_frequency == "daily":
        daily_rate = loan.interest_rate / 100 / 30  # Convert monthly percentage to daily decimal rate
        interest_due = loan.amount * daily_rate * days_elapsed
    elif loan.payment_frequency == "monthly":
        months_elapsed = days_elapsed / 30
        interest_due = loan.amount * (loan.interest_rate / 100) * months_elapsed
    else:
        interest_due = 0
    
    return interest_due

def get_remaining_balance(loan_id: int, db: Session) -> float:
    """
    Computes the remaining balance for a given loan, including simple interest accrued up to today.
    
    :param loan_id: ID of the loan.
    :param db: Database session.
    :return: Outstanding loan balance (total due - total payments).
    """
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        return None  # Loan not found
    
    total_paid = db.query(func.coalesce(func.sum(Payment.amount_paid), 0))\
                   .filter(Payment.loan_id == loan_id).scalar()
    
    # Calculate total due including simple interest up to today
    as_of_date = date.today()
    days_elapsed = (as_of_date - loan.loan_date).days
    months_elapsed = days_elapsed / 30  # approximate
    total_due = loan.amount * (1 + (loan.interest_rate / 100) * months_elapsed)
    
    remaining_balance = round(max(total_due - total_paid, 0), 2)
    
    return remaining_balance
