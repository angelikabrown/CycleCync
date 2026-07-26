from fastapi import APIRouter
from app.schemas.user import UserCreate

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register_user(user: UserCreate):

    return {
        "message": "User received",
        "username": user.username,
        "email": user.email
    }