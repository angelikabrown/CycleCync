from calendar import monthrange
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.daily_check_in import DailyCheckIn
from app.models.user import User
from app.services.daily_checkin_service import get_cycle_day


def get_calendar_days(
    db: Session,
    current_user: User,
    year: int,
    month: int,
):
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])

    checkins = db.execute(
        select(DailyCheckIn)
        .where(
            DailyCheckIn.user_id == current_user.id,
            DailyCheckIn.date >= first_day,
            DailyCheckIn.date <= last_day,
        )
        .order_by(DailyCheckIn.date)
    ).scalars().all()

    checkins_by_date = {
        checkin.date: checkin
        for checkin in checkins
    }

    calendar_days = []

    current_date = first_day

    while current_date <= last_day:
        checkin = checkins_by_date.get(current_date)

        calendar_days.append({
            "date": current_date,
            "cycle_day": get_cycle_day(
                db,
                current_user,
                current_date
            ),
            "period": checkin.period if checkin else False,
            "checkin": checkin,
        })

        current_date += timedelta(days=1)

    return calendar_days