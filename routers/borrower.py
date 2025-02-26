from fastapi import APIRouter

router = APIRouter(prefix="/borrowers", tags=["borrowers"])

@router.get("/")
def read_borrowers():
    return {"message": "Borrower router working"}
