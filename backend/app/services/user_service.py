from app.utils.security import hash_password
from fastapi import HTTPException

from app.models.user import User
from app.schemas.user import UserCreate
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