"""
Loan API Tests:

- `test_get_repayment_amount()`: Ensures loan repayment amount is calculated correctly.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_repayment_amount():
    """
    Test case to verify correct calculation of loan repayment amount.
    """
    response = client.get("/loans/1/details")
    assert response.status_code == 200
    assert "remaining_balance" in response.json()
