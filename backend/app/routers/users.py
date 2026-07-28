from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserResponse
from app.services.user_service import create_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=Token)
def register_user(user: UserCreate,
                  db: Session = Depends(get_db)):
    
 
    new_user = create_user(db, user)

    return new_user