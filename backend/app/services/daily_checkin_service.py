from http.client import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.daily_check_in import DailyCheckIn
from app.models.user import User
from app.utils.auth import get_current_user
from app.schemas.daily_check_in import DailyCheckInCreate


def create_daily_checkin(db: Session, daily_check_in: DailyCheckInCreate, current_user: User):
    """
    Create a new daily check-in for the current user.


    Args:
        db (Session): The database session.
        daily_check_in (DailyCheckInCreate): The daily check-in data.
        current_user (User): The currently authenticated user.
    
    Returns:
        DailyCheckIn: The created daily check-in instance.
    """
    
    existing_checkin = db.execute(
        select(DailyCheckIn).where(
            DailyCheckIn.user_id == current_user.id,
            DailyCheckIn.date == daily_check_in.date,
        )
        ).scalar_one_or_none()
    
    if existing_checkin is not None:
        raise HTTPException(status_code=400, detail="Daily check-in for this date already exists")
    
    new_checkin = DailyCheckIn(
        date = daily_check_in.date, 
        cycle_day=daily_check_in.cycle_day, 
        bbt=daily_check_in.bbt, 
        mood=daily_check_in.mood, 
        energy_level=daily_check_in.energy_level, 
        sleep_quality=daily_check_in.sleep_quality, 
        notes=daily_check_in.notes, 
        user_id=current_user.id)
    
    db.add(new_checkin)
    db.commit()
    db.refresh(new_checkin)

    return new_checkin
    
def get_daily_checkins(
    db: Session,
    current_user: User):
    """
    Retrieve all daily check-ins for the current user.

    Args:
        db (Session): The database session.
        current_user (User): The currently authenticated user.

    Returns:
        List[DailyCheckIn]: A list of daily check-ins for the current user.
    """
    daily_checkins = db.execute(
        select(DailyCheckIn).where(DailyCheckIn.user_id == current_user.id).order_by(DailyCheckIn.date.desc())
    ).scalars().all()

    return daily_checkins