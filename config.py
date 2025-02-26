import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

DATABASE_NAME = os.getenv("DATABASE_NAME", "money_lending")
DATABASE_USER = os.getenv("DATABASE_USER", "admin")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "password")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")

DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"
