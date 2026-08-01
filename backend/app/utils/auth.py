import select
from app.config import ALGORITHM, SECRET_KEY
from app.utils import jwt
from app.models.user import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db

# Define the OAuth2PasswordBearer instance with the token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):  
    '''
    Retrieve the current user based on the provided JWT token.
    
    Args:
        token (str): The JWT token extracted from the request.
        db (Session): The database session.    
    
    Returns:
        User: The user object corresponding to the token.
    
    '''
    # Decode the JWT token and retrieve the user from the database
    try:
        payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
        )
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    # Extract the user ID from the token payload
    user_id = payload.get("sub")

    # If the user ID is not present in the token payload, raise an HTTPException
    user = db.execute(select(User).where(User.id == int(user_id))).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # If the user is found, return the user object
    return user
    
