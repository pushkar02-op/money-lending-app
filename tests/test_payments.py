"""
Payment API Tests:

- `test_record_payment_success()`: Ensures an agent can record a valid payment.
- `test_overpayment_rejected()`: Prevents payments that exceed the remaining balance.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_record_payment_success():
    """
    Test case to verify successful payment recording.
    """
    response = client.post("/payments/pay", json={"loan_id": 1, "amount_paid": 500})
    assert response.status_code == 200
    assert "remaining_balance" in response.json()

def test_overpayment_rejected():
    """
    Test case to ensure payments cannot exceed the remaining balance.
    """
    response = client.post("/payments/pay", json={"loan_id": 1, "amount_paid": 999999})
    assert response.status_code == 400
    assert response.json()["detail"] == "Payment exceeds remaining balance."
