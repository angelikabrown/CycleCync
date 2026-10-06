from datetime import date

from pydantic import BaseModel

from app.schemas.daily_check_in import DailyCheckInResponse


class CalendarDay(BaseModel):
    date: date
    cycle_day: int | None = None
    period: bool
    checkin: DailyCheckInResponse | None = None