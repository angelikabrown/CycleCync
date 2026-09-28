from dataclasses import Field
from typing import Literal
from pydantic import BaseModel, Field
from datetime import date

class DailyCheckInCreate(BaseModel):
    date: date
    cycle_day: int | None = Field(default=None, ge=1)
    bbt: float | None = None
    mood: Literal["Excellent", "Good", "OK", "Bad", "Very Bad"] | None = None
    energy_level: str | None = None
    sleep_quality: str | None = None
    notes: str | None = None


class DailyCheckInResponse(BaseModel):
    id: int
    date: date
    cycle_day: int | None = Field(default=None, ge=1)
    bbt: float | None = None
    mood: str | None = None
    energy_level: str | None = None
    sleep_quality: str | None = None
    notes: str | None = None