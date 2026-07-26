from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user_services import create_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register_user(user: UserCreate,
                  db: Session = Depends(get_db)):
    
 
    new_user = create_user(db, user)

    return {
        "message": "User created successfully",
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }