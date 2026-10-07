from datetime import date

from app.models.daily_check_in import DailyCheckIn
from app.services.cycle_metrics_service import (
    get_period_starts,
    get_period_lengths,
    get_cycle_lengths,
    get_cycle_metrics,
)


def test_get_period_starts():

    # Test that get_period_starts correctly identifies the start dates of periods from a list of period dates.

    period_dates = [
        date(2026, 9, 1),
        date(2026, 9, 2),
        date(2026, 9, 3),
        date(2026, 9, 29),
        date(2026, 9, 30),
        date(2026, 10, 1),
    ]

    result = get_period_starts(period_dates)

    assert result == [
        date(2026, 9, 1),
        date(2026, 9, 29),
    ]


def test_get_period_lengths():
    period_dates = [
        date(2026, 9, 1),
        date(2026, 9, 2),
        date(2026, 9, 3),
        date(2026, 9, 29),
        date(2026, 9, 30),
    ]

    result = get_period_lengths(period_dates)

    assert result == [3, 2]


def test_get_cycle_lengths():
    period_starts = [
        date(2026, 9, 1),
        date(2026, 9, 29),
        date(2026, 10, 28),
    ]

    result = get_cycle_lengths(period_starts)

    assert result == [28, 29]


def test_cycle_metrics_with_multiple_completed_cycles(db):
    user = db.query(
        # Replace with your normal User creation if needed
        __import__("app.models.user", fromlist=["User"]).User
    ).first()

    if user is None:
        from app.models.user import User

        user = User(
            username="metricsuser",
            email="metrics@example.com",
            hashed_password="test",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    period_dates = [
        # Cycle 1 period: 3 days
        date(2026, 7, 1),
        date(2026, 7, 2),
        date(2026, 7, 3),

        # Cycle 2 period: 4 days
        date(2026, 7, 29),
        date(2026, 7, 30),
        date(2026, 7, 31),
        date(2026, 8, 1),

        # Cycle 3 period: current/incomplete
        date(2026, 8, 28),
        date(2026, 8, 29),
    ]

    for period_date in period_dates:
        db.add(
            DailyCheckIn(
                user_id=user.id,
                date=period_date,
                period=True,
            )
        )

    db.commit()

    result = get_cycle_metrics(db, user)

    assert result["cycles_tracked"] == 3
    assert result["completed_cycles"] == 2

    assert result["average_cycle_length"] == 29
    assert result["shortest_cycle_length"] == 28
    assert result["longest_cycle_length"] == 30

    assert result["average_period_length"] == 3
    assert result["shortest_period_length"] == 2
    assert result["longest_period_length"] == 4


def test_cycle_metrics_with_only_one_cycle(db):

    # Test that get_cycle_metrics returns the correct metrics when there is only one cycle tracked for the user.
    
    from app.models.user import User

    user = User(
        username="singlecycle",
        email="singlecycle@example.com",
        hashed_password="test",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    for period_date in [
        date(2026, 9, 1),
        date(2026, 9, 2),
        date(2026, 9, 3),
    ]:
        db.add(
            DailyCheckIn(
                user_id=user.id,
                date=period_date,
                period=True,
            )
        )

    db.commit()

    result = get_cycle_metrics(db, user)

    assert result["cycles_tracked"] == 1
    assert result["completed_cycles"] == 0

    assert result["average_cycle_length"] is None
    assert result["shortest_cycle_length"] is None
    assert result["longest_cycle_length"] is None

    assert result["average_period_length"] == 3
    assert result["shortest_period_length"] == 3
    assert result["longest_period_length"] == 3


def test_cycle_metrics_with_no_period_history(db):

    # Test that get_cycle_metrics returns the correct metrics when there is no period history for the user.

    from app.models.user import User

    user = User(
        username="nocycle",
        email="nocycle@example.com",
        hashed_password="test",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    result = get_cycle_metrics(db, user)

    assert result == {
        "cycles_tracked": 0,
        "completed_cycles": 0,
        "average_cycle_length": None,
        "shortest_cycle_length": None,
        "longest_cycle_length": None,
        "average_period_length": None,
        "shortest_period_length": None,
        "longest_period_length": None,
    }