import logging
from datetime import datetime, timedelta
from jose import jwt
from config import SECRET_KEY, ALGORITHM

logger = logging.getLogger(__name__)

def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        logger.error(f"Error creating access token: {e}")
        raise
