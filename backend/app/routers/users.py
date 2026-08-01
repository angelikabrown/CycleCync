
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import LoginRequest, Token, UserCreate, UserResponse
from app.utils.auth import get_current_user
from app.services.user_service import create_user, login_user

router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate,
                  db: Session = Depends(get_db)):
    """
    Register a new user in the database.
    Args:
        user (UserCreate): The user data to create.
        db (Session): The database session.
    Returns:
        UserResponse: The created user instance.
    """
    
 
    new_user = create_user(db, user)

    return new_user

@router.post("/login", response_model=Token)
def login(login: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user based on email and password.

    Args:
        login (LoginRequest): The login request data.
        db (Session): The database session.
    Returns:
        Token: The access token and token type.
    """

    return login_user(db, login)

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user