from datetime import datetime, timedelta, timezone

from jose import jwt

from app.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

def create_access_token(user_id: int) -> str:
    

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
    "sub": str(user_id),
    "exp": expire
}
    

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)