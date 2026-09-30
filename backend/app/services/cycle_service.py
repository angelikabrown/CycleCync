from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.daily_check_in import DailyCheckIn
from app.models.user import User


def get_cycle_day(
    db: Session,
    current_user: User,
    target_date: date,
) -> int | None:
    """
    Calculate the cycle day for a user on a specific date.

    The most recent period day on or before target_date
    establishes CD1.

    Returns None if the user has no recorded period start
    before or on the target date.
    """

    latest_period = db.execute(
        select(DailyCheckIn)
        .where(
            DailyCheckIn.user_id == current_user.id,
            DailyCheckIn.period.is_(True),
            DailyCheckIn.date <= target_date,
        )
        .order_by(DailyCheckIn.date.desc())
    ).scalars().first()

    if latest_period is None:
        return None

    return (target_date - latest_period.date).days + 1