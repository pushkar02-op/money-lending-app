from pydantic import BaseModel, PositiveFloat

class PaymentCreate(BaseModel):
    loan_id: int
    amount_paid: PositiveFloat  # Ensures amount is positive
