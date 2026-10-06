from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.calendar import CalendarDay
from app.services.calendar_service import get_calendar_days
from app.utils.auth import get_current_user


router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"]
)


@router.get("/", response_model=list[CalendarDay])
def get_calendar(
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_calendar_days(
        db,
        current_user,
        year,
        month,
    )