from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.daily_check_in import DailyCheckIn
from app.models.user import User


def get_cycle_day(
    db: Session,
    current_user: User,
    target_date: date,
) -> int | None:

    period_dates = db.execute(
        select(DailyCheckIn.date)
        .where(
            DailyCheckIn.user_id == current_user.id,
            DailyCheckIn.period.is_(True),
            DailyCheckIn.date <= target_date,
        )
        .order_by(DailyCheckIn.date.desc())
    ).scalars().all()

    if not period_dates:
        return None

    period_start = period_dates[0]

    for i in range(1, len(period_dates)):
        expected_date = period_start - timedelta(days=1)

        if period_dates[i] == expected_date:
            period_start = period_dates[i]
        else:
            break

    return (target_date - period_start).days + 1