from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.daily_check_in import DailyCheckIn
from app.models.user import User
from app.schemas.daily_check_in import DailyCheckInCreate
from app.services.cycle_service import get_cycle_day


def create_daily_checkin(db, daily_check_in, current_user):
    existing_checkin = db.execute(
        select(DailyCheckIn).where(
            DailyCheckIn.user_id == current_user.id,
            DailyCheckIn.date == daily_check_in.date,
        )
    ).scalar_one_or_none()

    if existing_checkin is not None:
        raise HTTPException(
            status_code=400,
            detail="Daily check-in for this date already exists"
        )

    cycle_day = get_cycle_day(
        db,
        current_user,
        daily_check_in.date
    )

    new_checkin = DailyCheckIn(
        user_id=current_user.id,
        date=daily_check_in.date,
        cycle_day=cycle_day,
        period=daily_check_in.period,
        bbt=daily_check_in.bbt,
        mood=daily_check_in.mood,
        energy_level=daily_check_in.energy_level,
        sleep_quality=daily_check_in.sleep_quality,
        notes=daily_check_in.notes,
    )

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

def delete_daily_checkin(
    db: Session,
    checkin_id: int,
    current_user: User
):
    """
    Delete a daily check-in belonging to the current user.

    Args:
        db (Session): The database session.
        checkin_id (int): The ID of the check-in to delete.
        current_user (User): The currently authenticated user.

    Returns:
        DailyCheckIn: The deleted check-in.

    Raises:
        HTTPException: If the check-in does not exist or does not belong
        to the current user.
    """

    checkin = db.execute(
        select(DailyCheckIn).where(
            DailyCheckIn.id == checkin_id,
            DailyCheckIn.user_id == current_user.id
        )
    ).scalar_one_or_none()

    if checkin is None:
        raise HTTPException(
            status_code=404,
            detail="Daily check-in not found"
        )

    db.delete(checkin)
    db.commit()

    return checkin

def update_daily_checkin(
    db: Session,
    checkin_id: int,
    daily_check_in: DailyCheckInCreate,
    current_user: User
):
    """
    Update a daily check-in belonging to the current user.
    """

    checkin = db.execute(
        select(DailyCheckIn).where(
            DailyCheckIn.id == checkin_id,
            DailyCheckIn.user_id == current_user.id
        )
    ).scalar_one_or_none()

    if checkin is None:
        raise HTTPException(
            status_code=404,
            detail="Daily check-in not found"
        )

    # Update the user-entered fields
    checkin.date = daily_check_in.date
    checkin.period = daily_check_in.period
    checkin.bbt = daily_check_in.bbt
    checkin.mood = daily_check_in.mood
    checkin.energy_level = daily_check_in.energy_level
    checkin.sleep_quality = daily_check_in.sleep_quality
    checkin.notes = daily_check_in.notes

    # Recalculate cycle day
    if daily_check_in.period:
        checkin.cycle_day = 1
    else:
        checkin.cycle_day = get_cycle_day(
            db,
            current_user,
            daily_check_in.date
        )

    db.commit()
    db.refresh(checkin)

    return checkin