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



#  This test checks the behavior of the daily check-in endpoint when attempting to create a duplicate check-in for the same date. It first registers a user, logs in to obtain a JWT token, and then sends a POST request to the /daily_checkins/checkin endpoint with the token included in the Authorization header. The test verifies that the first check-in creation is successful (status code 200) and that the second attempt to create a check-in for the same date fails (status code 400).
def test_create_duplicate_checkin(client):
    # Register user
    client.post(
        "/users/register",
        json={
            "username": "duplicatecheckin",
            "email": "duplicatecheckin@example.com",
            "password": "password123"
        }
    )

    # Login
    login_response = client.post(
        "/users/login",
        data={
            "username": "duplicatecheckin@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    checkin = {
        "date": "2026-09-27",
        "cycle_day": 10,
        "bbt": 97.5,
        "mood": "Good",
        "energy_level": "High",
        "sleep_quality": "Good",
        "notes": "Test check-in"
    }

    # First check-in should succeed
    response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json=checkin
    )

    assert response.status_code == 200

    # Second check-in for the same date should fail
    response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json=checkin
    )

    assert response.status_code == 400