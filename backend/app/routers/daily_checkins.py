from app.database import get_db
from app.models.user import User
from app.schemas.daily_check_in import DailyCheckInCreate, DailyCheckInResponse
from app.utils.auth import get_current_user
from app.services.daily_checkin_service import create_daily_checkin, get_daily_checkins
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


router = APIRouter(prefix="/daily_checkins", tags=["Daily Check-ins"])

@router.post("/checkin", response_model=DailyCheckInResponse)
def daily_check_in(daily_check_in: DailyCheckInCreate, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """
    Create a new daily check-in for the current user.

    Args:
        daily_check_in (DailyCheckInCreate): The daily check-in data.
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        dict: A success message indicating that the daily check-in was created.
    """

    # Create a new DailyCheckIn instance
    new_check_in = create_daily_checkin(db, daily_check_in, current_user)

    return new_check_in

@router.get("/", response_model=list[DailyCheckInResponse])
def get_daily_check_ins(db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """
    Retrieve all daily check-ins for the current user.

    Args:
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        list[DailyCheckInResponse]: A list of daily check-ins for the current user.
    """

    daily_check_ins = get_daily_checkins(db, current_user)

    return daily_check_ins
