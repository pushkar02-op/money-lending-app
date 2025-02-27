# main.py
import logging
from fastapi import FastAPI
from auth.routes import router as auth_router
from routers.user import router as user_router  # Import the user router
from database import engine
from models.base import Base

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")

app.include_router(auth_router)
app.include_router(user_router)  # Include the user router

@app.get("/")
def root():
    return {"message": "Money Lending App is running"}
