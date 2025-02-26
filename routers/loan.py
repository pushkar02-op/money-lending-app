from fastapi import APIRouter

router = APIRouter(prefix="/loans", tags=["loans"])


@router.get("/")
def read_loans():
    return {"message": "Loan router working"}
