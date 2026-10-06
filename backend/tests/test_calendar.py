def get_token(client, email):
    login_response = client.post(
        "/users/login",
        data={
            "username": email,
            "password": "password123"
        }
    )

    return login_response.json()["access_token"]


def test_calendar_requires_authentication(client):
    response = client.get(
        "/calendar/",
        params={
            "year": 2026,
            "month": 10
        }
    )

    assert response.status_code == 401

def test_calendar_returns_every_day_of_month(client):
    # Register user
    client.post(
        "/users/register",
        json={
            "username": "calendaruser",
            "email": "calendar@example.com",
            "password": "password123"
        }
    )

    token = get_token(client, "calendar@example.com")

    response = client.get(
        "/calendar/",
        params={
            "year": 2026,
            "month": 10
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 31
    assert data[0]["date"] == "2026-10-01"
    assert data[-1]["date"] == "2026-10-31"

def test_calendar_cycle_day_continues_without_checkin(client):
    # Register user
    client.post(
        "/users/register",
        json={
            "username": "calendarcycleuser",
            "email": "calendarcycle@example.com",
            "password": "password123"
        }
    )

    token = get_token(client, "calendarcycle@example.com")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Start the cycle
    client.post(
        "/daily_checkins/checkin",
        headers=headers,
        json={
            "date": "2026-10-01",
            "period": True
        }
    )

    # Get calendar
    response = client.get(
        "/calendar/",
        params={
            "year": 2026,
            "month": 10
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    # October 1 = CD1
    assert data[0]["cycle_day"] == 1

    # October 2 has NO check-in, but should still be CD2
    assert data[1]["cycle_day"] == 2
    assert data[1]["checkin"] is None

    # October 3 = CD3, also without a check-in
    assert data[2]["cycle_day"] == 3
    assert data[2]["checkin"] is None

def test_calendar_period_days_have_correct_cycle_days(client):
    client.post(
        "/users/register",
        json={
            "username": "calendarperioduser",
            "email": "calendarperiod@example.com",
            "password": "password123"
        }
    )

    token = get_token(client, "calendarperiod@example.com")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Period starts October 1
    client.post(
        "/daily_checkins/checkin",
        headers=headers,
        json={
            "date": "2026-10-01",
            "period": True
        }
    )

    # Period continues October 2
    client.post(
        "/daily_checkins/checkin",
        headers=headers,
        json={
            "date": "2026-10-02",
            "period": True
        }
    )

    # Period continues October 3
    client.post(
        "/daily_checkins/checkin",
        headers=headers,
        json={
            "date": "2026-10-03",
            "period": True
        }
    )

    response = client.get(
        "/calendar/",
        params={
            "year": 2026,
            "month": 10
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data[0]["cycle_day"] == 1
    assert data[0]["period"] is True

    assert data[1]["cycle_day"] == 2
    assert data[1]["period"] is True

    assert data[2]["cycle_day"] == 3
    assert data[2]["period"] is True

def test_calendar_new_period_starts_new_cycle(client):
    client.post(
        "/users/register",
        json={
            "username": "newcycleuser",
            "email": "newcycle@example.com",
            "password": "password123"
        }
    )

    token = get_token(client, "newcycle@example.com")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # First cycle starts October 1
    client.post(
        "/daily_checkins/checkin",
        headers=headers,
        json={
            "date": "2026-10-01",
            "period": True
        }
    )

    # Second cycle starts October 19
    client.post(
        "/daily_checkins/checkin",
        headers=headers,
        json={
            "date": "2026-10-19",
            "period": True
        }
    )

    response = client.get(
        "/calendar/",
        params={
            "year": 2026,
            "month": 10
        },
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    # Before the new period
    assert data[17]["date"] == "2026-10-18"
    assert data[17]["cycle_day"] == 18

    # New period resets cycle
    assert data[18]["date"] == "2026-10-19"
    assert data[18]["cycle_day"] == 1
    assert data[18]["period"] is True

    # Cycle continues after new period
    assert data[19]["date"] == "2026-10-20"
    assert data[19]["cycle_day"] == 2

def test_calendar_no_period_history_returns_null_cycle_day(client):
    client.post(
        "/users/register",
        json={
            "username": "nocycleuser",
            "email": "nocycle@example.com",
            "password": "password123"
        }
    )

    token = get_token(client, "nocycle@example.com")

    response = client.get(
        "/calendar/",
        params={
            "year": 2026,
            "month": 10
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 31
    assert data[0]["cycle_day"] is None
    assert data[15]["cycle_day"] is None
    assert data[30]["cycle_day"] is None

def test_user_cannot_see_another_users_calendar_checkins(client):
    # Register User A
    client.post(
        "/users/register",
        json={
            "username": "calendarusera",
            "email": "calendarusera@example.com",
            "password": "password123"
        }
    )

    token_a = get_token(client, "calendarusera@example.com")

    # Register User B
    client.post(
        "/users/register",
        json={
            "username": "calendaruserb",
            "email": "calendaruserb@example.com",
            "password": "password123"
        }
    )

    token_b = get_token(client, "calendaruserb@example.com")

    # User B creates a period check-in
    client.post(
        "/daily_checkins/checkin",
        headers={
            "Authorization": f"Bearer {token_b}"
        },
        json={
            "date": "2026-10-01",
            "period": True,
            "mood": "Good"
        }
    )

    # User A retrieves their calendar
    response = client.get(
        "/calendar/",
        params={
            "year": 2026,
            "month": 10
        },
        headers={
            "Authorization": f"Bearer {token_a}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    # User A should see the calendar dates,
    # but not User B's check-in.
    assert data[0]["date"] == "2026-10-01"
    assert data[0]["cycle_day"] is None
    assert data[0]["period"] is False
    assert data[0]["checkin"] is None

def test_calendar_invalid_month(client):
    client.post(
        "/users/register",
        json={
            "username": "invalidmonthuser",
            "email": "invalidmonth@example.com",
            "password": "password123"
        }
    )

    token = get_token(client, "invalidmonth@example.com")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Month 0
    response = client.get(
        "/calendar/",
        params={
            "year": 2026,
            "month": 0
        },
        headers=headers
    )

    assert response.status_code == 422

    # Month 13
    response = client.get(
        "/calendar/",
        params={
            "year": 2026,
            "month": 13
        },
        headers=headers
    )

    assert response.status_code == 422