from fastapi import FastAPI
from auth.routes import router as auth_router
from database import engine
from models.base import Base

# Initialize app
app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include authentication routes
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Money Lending App is running"}
