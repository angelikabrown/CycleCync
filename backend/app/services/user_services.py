

from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session

def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to create.

    Returns:
        User: The created user instance.
    """
    new_user = User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user