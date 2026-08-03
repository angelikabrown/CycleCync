from pydantic import BaseModel
from datetime import date

class DailyCheckInCreate(BaseModel):
    date: date
    cycle_day: int | None = None
    bbt: float | None = None
    mood: str | None = None
    energy_level: str | None = None
    sleep_quality: str | None = None
    notes: str | None = None


class DailyCheckInResponse(BaseModel):
    id: int
    date: date
    cycle_day: int | None = None
    bbt: float | None = None
    mood: str | None = None
    energy_level: str | None = None
    sleep_quality: str | None = None
    notes: str | None = None