from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register_user(user: UserCreate,
                  db: Session = Depends(get_db)):
    
    #create a new user instance
    new_user = User(username=user.username, email=user.email, password=user.password)

    return {
        "message": "User received",
        "username": user.username,
        "email": user.email
    }