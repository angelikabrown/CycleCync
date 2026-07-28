from app.utils.jwt import create_access_token
from fastapi import HTTPException

from app.utils.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import LoginRequest, UserCreate
from sqlalchemy.orm import Session
from sqlalchemy import select

def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to create.

    Returns:
        User: The created user instance.
    """
    # Check if the username already exists
    existing_user = db.execute(select(User).where(User.username == user.username)).scalar_one_or_none()

    if existing_user is not None:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    #check if the email already exists
    existing_email = db.execute(select(User).where(User.email == user.email)).scalar_one_or_none()

    if existing_email is not None:
        raise HTTPException(status_code=400, detail="Email already exists") 
    

    new_user = User(username=user.username, email=user.email, hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def login_user(db: Session, login: LoginRequest):
    """
    Authenticate a user based on email and password.

    Args:
        db (Session): The database session.
        login (LoginRequest): The login request data.
    """
    user = db.execute(select(User).where(User.email == login.email)).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(login.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    token = create_access_token(user.id)

    return {
    "access_token": token,
    "token_type": "bearer"
}