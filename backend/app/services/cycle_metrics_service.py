from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.daily_check_in import DailyCheckIn
from app.models.user import User


def get_period_dates(
    db: Session,
    current_user: User,
) -> list:
    return db.execute(
        select(DailyCheckIn.date)
        .where(
            DailyCheckIn.user_id == current_user.id,
            DailyCheckIn.period.is_(True),
        )
        .order_by(DailyCheckIn.date)
    ).scalars().all()


def get_period_starts(period_dates: list) -> list:
    if not period_dates:
        return []

    starts = [period_dates[0]]

    for current_date, previous_date in zip(
        period_dates[1:],
        period_dates[:-1],
    ):
        if current_date != previous_date + timedelta(days=1):
            starts.append(current_date)

    return starts


def get_period_lengths(period_dates: list) -> list[int]:
    if not period_dates:
        return []

    lengths = []
    current_length = 1

    for current_date, previous_date in zip(
        period_dates[1:],
        period_dates[:-1],
    ):
        if current_date == previous_date + timedelta(days=1):
            current_length += 1
        else:
            lengths.append(current_length)
            current_length = 1

    lengths.append(current_length)

    return lengths


def get_cycle_lengths(period_starts: list) -> list[int]:
    if len(period_starts) < 2:
        return []

    return [
        (current_start - previous_start).days
        for previous_start, current_start in zip(
            period_starts[:-1],
            period_starts[1:],
        )
    ]


def get_cycle_metrics(
    db: Session,
    current_user: User,
) -> dict:

    period_dates = get_period_dates(db, current_user)

    if not period_dates:
        return {
            "cycles_tracked": 0,
            "completed_cycles": 0,
            "average_cycle_length": None,
            "shortest_cycle_length": None,
            "longest_cycle_length": None,
            "average_period_length": None,
            "shortest_period_length": None,
            "longest_period_length": None,
        }

    period_starts = get_period_starts(period_dates)
    period_lengths = get_period_lengths(period_dates)
    cycle_lengths = get_cycle_lengths(period_starts)

    return {
        "cycles_tracked": len(period_starts),
        "completed_cycles": len(cycle_lengths),

        "average_cycle_length": (
            sum(cycle_lengths) / len(cycle_lengths)
            if cycle_lengths
            else None
        ),

        "shortest_cycle_length": (
            min(cycle_lengths)
            if cycle_lengths
            else None
        ),

        "longest_cycle_length": (
            max(cycle_lengths)
            if cycle_lengths
            else None
        ),

        "average_period_length": (
            sum(period_lengths) / len(period_lengths)
            if period_lengths
            else None
        ),

        "shortest_period_length": (
            min(period_lengths)
            if period_lengths
            else None
        ),

        "longest_period_length": (
            max(period_lengths)
            if period_lengths
            else None
        ),
    }