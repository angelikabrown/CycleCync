from datetime import date

from app.models.daily_check_in import DailyCheckIn
from app.models.user import User


def get_token(client, email):

    # Helper function to get an access token for a user. It logs in the user and retrieves the access token from the response.

    response = client.post(
        "/users/login",
        data={
            "username": email,
            "password": "password123",
        },
    )

    return response.json()["access_token"]


def test_cycle_metrics_requires_authentication(client):

    # Test that the /cycle-metrics/ endpoint requires authentication. It sends a GET request without an access token and checks that the response status code is 401 (Unauthorized).

    response = client.get("/cycle-metrics/")

    assert response.status_code == 401


def test_cycle_metrics_returns_metrics(client, db):

    # Test that the /cycle-metrics/ endpoint returns the correct metrics for a user with period history. It creates a user, adds period check-ins, and checks that the response contains the expected metrics.

    client.post(
        "/users/register",
        json={
            "username": "metricsapi",
            "email": "metricsapi@example.com",
            "password": "password123",
        },
    )

    token = get_token(client, "metricsapi@example.com")

    user = db.query(User).filter(
        User.email == "metricsapi@example.com"
    ).first()

    period_dates = [
        date(2026, 7, 1),
        date(2026, 7, 2),
        date(2026, 7, 3),

        date(2026, 7, 29),
        date(2026, 7, 30),
        date(2026, 7, 31),
        date(2026, 8, 1),

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

    response = client.get(
        "/cycle-metrics/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["cycles_tracked"] == 3
    assert data["completed_cycles"] == 2

    assert data["average_cycle_length"] == 29
    assert data["shortest_cycle_length"] == 28
    assert data["longest_cycle_length"] == 30

    assert data["average_period_length"] == 3
    assert data["shortest_period_length"] == 2
    assert data["longest_period_length"] == 4


def test_cycle_metrics_user_isolation(client, db):

    # Test that the /cycle-metrics/ endpoint returns metrics only for the authenticated user. It creates two users, adds period check-ins for one user, and checks that the other user sees no metrics.
    
    client.post(
        "/users/register",
        json={
            "username": "userone",
            "email": "userone@example.com",
            "password": "password123",
        },
    )

    client.post(
        "/users/register",
        json={
            "username": "usertwo",
            "email": "usertwo@example.com",
            "password": "password123",
        },
    )

    user_one = db.query(User).filter(
        User.email == "userone@example.com"
    ).first()

    db.add(
        DailyCheckIn(
            user_id=user_one.id,
            date=date(2026, 7, 1),
            period=True,
        )
    )

    db.commit()

    token = get_token(client, "usertwo@example.com")

    response = client.get(
        "/cycle-metrics/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["cycles_tracked"] == 0
    assert data["completed_cycles"] == 0