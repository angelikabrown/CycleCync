from typing import Literal
from datetime import date

from pydantic import BaseModel, Field


class DailyCheckInCreate(BaseModel):
    date: date
    period: bool = False
    cycle_day: int | None = Field(default=None, ge=1)
    bbt: float | None = None
    mood: Literal["Excellent", "Good", "OK", "Bad", "Very Bad"] | None = None
    energy_level: Literal[
        "Very High",
        "High",
        "Moderate",
        "Low",
        "Very Low"
    ] | None = None
    sleep_quality: Literal[
        "Excellent",
        "Very Good",
        "Good",
        "Fair",
        "Poor"
    ] | None = None
    notes: str | None = None


class DailyCheckInResponse(BaseModel):
    id: int
    date: date
    period: bool
    cycle_day: int | None = Field(default=None, ge=1)
    bbt: float | None = None
    mood: str | None = None
    energy_level: str | None = None
    sleep_quality: str | None = None
    notes: str | None = None