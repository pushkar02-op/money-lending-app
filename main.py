import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth.routes import router as auth_router
from routers.user import router as user_router
from routers.loan import router as loan_router
from routers.borrower import router as borrower_router
from routers.payment import router as payment_router
from database import engine, SessionLocal
from models.base import Base
import os

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
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

    # Bootstrap the first admin if no admin exists
    try:
        db = SessionLocal()
        from models.user import User
        from auth.security import get_password_hash
        admin_exists = db.query(User).filter(User.role == "admin").first()
        if not admin_exists:
            first_admin_email = os.getenv("FIRST_ADMIN_EMAIL")
            first_admin_name = os.getenv("FIRST_ADMIN_NAME")
            first_admin_password = os.getenv("FIRST_ADMIN_PASSWORD")
            if first_admin_email and first_admin_name and first_admin_password:
                new_admin = User(
                    name=first_admin_name,
                    email=first_admin_email,
                    password_hash=get_password_hash(first_admin_password),
                    role="admin"
                )
                db.add(new_admin)
                db.commit()
                db.refresh(new_admin)
                logger.info("Bootstrap: First admin created successfully.")
                # Remove these environment variables for security
                os.environ.pop("FIRST_ADMIN_EMAIL", None)
                os.environ.pop("FIRST_ADMIN_NAME", None)
                os.environ.pop("FIRST_ADMIN_PASSWORD", None)
                logger.info("Bootstrap: First admin environment variables removed.")
            else:
                logger.info("Bootstrap: First admin environment variables not provided.")
    except Exception as e:
        logger.error(f"Bootstrap error: {e}")
    finally:
        db.close()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(loan_router)
app.include_router(borrower_router)
app.include_router(payment_router)
