import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from routers.user import router as user_router
from routers.loan import router as loan_router
from routers.borrower import router as borrower_router
from routers.payment import router as payment_router
from database import engine
from models.base import Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Configure CORS
origins = ["http://localhost", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(loan_router)
app.include_router(borrower_router)
app.include_router(payment_router)


