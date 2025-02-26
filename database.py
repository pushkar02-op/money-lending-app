import re
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL, DATABASE_NAME

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Ensure database exists
try:
    url_without_db = re.sub(r"/[^/]+$", "/", DATABASE_URL)
    engine_without_db = create_engine(url_without_db)
    with engine_without_db.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"))
    engine_without_db.dispose()
    logger.info(f"Database '{DATABASE_NAME}' ensured to exist.")
except Exception as e:
    logger.error(f"Error ensuring database exists: {e}")
    raise

# Create main engine and session
try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database engine and session created successfully.")
except Exception as e:
    logger.error(f"Error creating database engine or session: {e}")
    raise


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error during database session: {e}")
        raise
    finally:
        db.close()
