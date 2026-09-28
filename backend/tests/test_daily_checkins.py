
#
#  This is a test file for the daily check-in endpoint of the FastAPI application.
#  It uses pytest and the TestClient from FastAPI to simulate requests to the API.


#  The test_create_checkin function sends a POST request to the /daily_checkins/checkin endpoint with a JSON payload containing check-in data
def test_create_checkin_without_token(client):
    response = client.post(
        "/daily_checkins/checkin",
        json={
            "date": "2026-09-27",
            "cycle_day": 10,
            "bbt": 97.5,
            "mood": "Good",
            "energy_level": "High",
            "sleep_quality": "Good",
            "notes": "Test check-in"
        }
    )

    assert response.status_code == 401


#  This test checks the behavior of the daily check-in endpoint when a user is authenticated using a JWT token. It first registers a user, logs in to obtain a JWT token, and then sends a POST request to the /daily_checkins/checkin endpoint with the token included in the Authorization header. The test verifies that the check-in creation is successful (status code 200).
def test_create_checkin_with_token(client):
    # Register user
    client.post(
        "/users/register",
        json={
            "username": "checkinuser",
            "email": "checkin@example.com",
            "password": "password123"
        }
    )

    # Login
    login_response = client.post(
        "/users/login",
        data={
            "username": "checkin@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    # Create check-in using JWT
    response = client.post(
        "/daily_checkins/checkin",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date": "2026-09-27",
            "cycle_day": 10,
            "bbt": 97.5,
            "mood": "Good",
            "energy_level": "High",
            "sleep_quality": "Good",
            "notes": "Test check-in"
        }
    )

    assert response.status_code == 200



#  This test checks the behavior of the daily check-in endpoint when a user attempts to create a check-in with a negative cycle day. It first registers a user, logs in to obtain a JWT token, and then sends a POST request to the /daily_checkins/checkin endpoint with the token included in the Authorization header and a negative cycle day in the payload. The test verifies that the request fails (status code 422) due to validation errors.
def test_create_checkin_negative_cycle_day(client):
    # Register user
    client.post(
        "/users/register",
        json={
            "username": "negativecycleuser",
            "email": "negativecycle@example.com",
            "password": "password123"
        }
    )

    # Login
    login_response = client.post(
        "/users/login",
        data={
            "username": "negativecycle@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    # Try to create a check-in with a negative cycle day
    response = client.post(
        "/daily_checkins/checkin",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date": "2026-09-27",
            "cycle_day": -1,
            "bbt": 97.5,
            "mood": "Good",
            "energy_level": "High",
            "sleep_quality": "Good",
            "notes": "Invalid cycle day"
        }
    )

    assert response.status_code == 422


#  This test checks the behavior of the daily check-in endpoint when a user attempts to create a check-in with only the required fields. It first registers a user, logs in to obtain a JWT token, and then sends a POST request to the /daily_checkins/checkin endpoint with the token included in the Authorization header and only the required date field in the payload. The test verifies that the check-in creation is successful (status code 200).
def test_create_checkin_with_only_required_fields(client):
    # Register user
    client.post(
        "/users/register",
        json={
            "username": "minimaluser",
            "email": "minimal@example.com",
            "password": "password123"
        }
    )

    # Login
    login_response = client.post(
        "/users/login",
        data={
            "username": "minimal@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    # Create check-in with only required data
    response = client.post(
        "/daily_checkins/checkin",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date": "2026-09-27"
        }
    )

    assert response.status_code == 200


#  This test checks the behavior of the daily check-in endpoint when a user attempts to create a check-in with an invalid mood value. It first registers a user, logs in to obtain a JWT token, and then sends a POST request to the /daily_checkins/checkin endpoint with the token included in the Authorization header and an invalid mood value in the payload. The test verifies that the request fails (status code 422) due to validation errors.
def test_create_checkin_invalid_mood(client):
    client.post(
        "/users/register",
        json={
            "username": "invalidmood",
            "email": "invalidmood@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "invalidmood@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-27",
            "cycle_day": 5,
            "mood": "Terrible"
        }
    )

    assert response.status_code == 422