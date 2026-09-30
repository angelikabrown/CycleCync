from datetime import date

from app.models.user import User
from app.services.cycle_service import get_cycle_day
#
#  This is a test file for the daily check-in endpoint of the FastAPI application.
#  It uses pytest and the TestClient from FastAPI to simulate requests to the API.

def get_token(client, email):
    login_response = client.post(
        "/users/login",
        data={
            "username": email,
            "password": "password123"
        }
    )

    return login_response.json()["access_token"]


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

#  This test checks the behavior of the daily check-in endpoint when attempting to create a duplicate check-in for the same date. It first registers a user, logs in to obtain a JWT token, and then sends a POST request to the /daily_checkins/checkin endpoint with the token included in the Authorization header. The test verifies that the first check-in creation is successful (status code 200) and that the second attempt to create a check-in for the same date fails (status code 400).
def test_create_duplicate_checkin(client):
    # Register user
    client.post(
        "/users/register",
        json={
            "username": "duplicatecheckin",
            "email": "duplicatecheckin@example.com",
            "password": "password123"
        }
    )

    # Login
    login_response = client.post(
        "/users/login",
        data={
            "username": "duplicatecheckin@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    checkin = {
        "date": "2026-09-27",
        "cycle_day": 10,
        "bbt": 97.5,
        "mood": "Good",
        "energy_level": "High",
        "sleep_quality": "Good",
        "notes": "Test check-in"
    }

    # First check-in should succeed
    response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json=checkin
    )

    assert response.status_code == 200

    # Second check-in for the same date should fail
    response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json=checkin
    )

    assert response.status_code == 400


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


#  This test checks the behavior of the daily check-in endpoint when a user attempts to create a check-in with an invalid energy level value. It first registers a user, logs in to obtain a JWT token, and then sends a POST request to the /daily_checkins/checkin endpoint with the token included in the Authorization header and an invalid energy level value in the payload. The test verifies that the request fails (status code 422) due to validation errors.
def test_create_checkin_invalid_energy(client):
    client.post(
        "/users/register",
        json={
            "username": "invalidenergy",
            "email": "invalidenergy@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "invalidenergy@example.com",
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
            "energy_level": "Superhuman"
        }
    )

    assert response.status_code == 422


# This test checks the behavior of the daily check-in endpoint when a user attempts to create a check-in with an invalid energy level value. It first registers a user, logs in to obtain a JWT token, and then sends a POST request to the /daily_checkins/checkin endpoint with the token included in the Authorization header and an invalid energy level value in the payload. The test verifies that the request fails (status code 422) due to validation errors.
def test_create_checkin_invalid_sleep(client):
    client.post(
        "/users/register",
        json={
            "username": "invalidsleep",
            "email": "invalidsleep@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "invalidsleep@example.com",
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
            "sleep_quality": "Amazing"
        }
    )

    assert response.status_code == 422

#  This test checks the behavior of the daily check-in endpoint when a user attempts to retrieve their own check-ins. It first registers a user, logs in to obtain a JWT token, creates a check-in, and then sends a GET request to the /daily_checkins/ endpoint with the token included in the Authorization header. The test verifies that the retrieval is successful (status code 200) and that the returned data matches the created check-in.
def test_get_own_checkins(client):
    client.post(
        "/users/register",
        json={
            "username": "historyuser",
            "email": "history@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "history@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    # Create a check-in
    client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-27",
            "cycle_day": 5,
            "mood": "Good"
        }
    )

    # Retrieve check-ins
    response = client.get(
        "/daily_checkins/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["date"] == "2026-09-27"
    assert data[0]["cycle_day"] == 5



#  This test checks the behavior of the daily check-in endpoint when a user attempts to retrieve check-ins created by another user. It first registers two users (User A and User B), logs in both users to obtain their respective JWT tokens, and then has User B create a check-in. Finally, it sends a GET request to the /daily_checkins/ endpoint with User A's token included in the Authorization header. The test verifies that User A cannot see User B's check-ins (the returned data is an empty list).
def test_user_cannot_see_another_users_checkins(client):
    # Register User A
    client.post(
        "/users/register",
        json={
            "username": "usera",
            "email": "usera@example.com",
            "password": "password123"
        }
    )

    # Login User A
    login_a = client.post(
        "/users/login",
        data={
            "username": "usera@example.com",
            "password": "password123"
        }
    )

    token_a = login_a.json()["access_token"]

    # Register User B
    client.post(
        "/users/register",
        json={
            "username": "userb",
            "email": "userb@example.com",
            "password": "password123"
        }
    )

    # Login User B
    login_b = client.post(
        "/users/login",
        data={
            "username": "userb@example.com",
            "password": "password123"
        }
    )

    token_b = login_b.json()["access_token"]

    # User B creates a check-in
    client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token_b}"},
        json={
            "date": "2026-09-27",
            "cycle_day": 10,
            "mood": "Good"
        }
    )

    # User A retrieves their check-ins
    response = client.get(
        "/daily_checkins/",
        headers={"Authorization": f"Bearer {token_a}"}
    )

    assert response.status_code == 200
    assert response.json() == []


#  This test checks the behavior of the daily check-in endpoint when a user creates multiple check-ins and then retrieves their history. It first registers a user, logs in to obtain a JWT token, creates two check-ins on different dates, and then sends a GET request to the /daily_checkins/ endpoint with the token included in the Authorization header. The test verifies that both check-ins are returned in the response (status code 200) and that the returned data matches the created check-ins.
def test_get_multiple_checkins(client):
    # Register user
    client.post(
        "/users/register",
        json={
            "username": "multipleuser",
            "email": "multiple@example.com",
            "password": "password123"
        }
    )

    # Login
    login_response = client.post(
        "/users/login",
        data={
            "username": "multiple@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Create first check-in
    client.post(
        "/daily_checkins/checkin",
        headers=headers,
        json={
            "date": "2026-09-25",
            "cycle_day": 3,
            "mood": "Good"
        }
    )

    # Create second check-in
    client.post(
        "/daily_checkins/checkin",
        headers=headers,
        json={
            "date": "2026-09-26",
            "cycle_day": 4,
            "mood": "Excellent"
        }
    )

    # Retrieve history
    response = client.get(
        "/daily_checkins/",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["date"] == "2026-09-26"
    assert data[1]["date"] == "2026-09-25"



def test_delete_own_checkin(client):
    client.post(
        "/users/register",
        json={
            "username": "deleteuser",
            "email": "delete@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "delete@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-28",
            "cycle_day": 6,
            "mood": "Good"
        }
    )

    checkin_id = create_response.json()["id"]

    response = client.delete(
        f"/daily_checkins/{checkin_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == checkin_id


def test_deleted_checkin_is_gone(client):
    client.post(
        "/users/register",
        json={
            "username": "goneuser",
            "email": "gone@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "gone@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-28",
            "cycle_day": 6,
            "mood": "Good"
        }
    )

    checkin_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/daily_checkins/{checkin_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert delete_response.status_code == 200

    history_response = client.get(
        "/daily_checkins/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert history_response.status_code == 200

    data = history_response.json()

    assert all(
        checkin["id"] != checkin_id
        for checkin in data
    )


def test_user_cannot_delete_another_users_checkin(client):
    # Create first user
    client.post(
        "/users/register",
        json={
            "username": "firstuser",
            "email": "first@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "first@example.com",
            "password": "password123"
        }
    )

    first_token = login_response.json()["access_token"]

    # Create first user's check-in
    create_response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {first_token}"},
        json={
            "date": "2026-09-28",
            "cycle_day": 6,
            "mood": "Good"
        }
    )

    checkin_id = create_response.json()["id"]

    # Create second user
    client.post(
        "/users/register",
        json={
            "username": "seconduser",
            "email": "second@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "second@example.com",
            "password": "password123"
        }
    )

    second_token = login_response.json()["access_token"]

    # Second user attempts to delete first user's check-in
    response = client.delete(
        f"/daily_checkins/{checkin_id}",
        headers={"Authorization": f"Bearer {second_token}"}
    )

    assert response.status_code == 404

def test_delete_nonexistent_checkin(client):
    client.post(
        "/users/register",
        json={
            "username": "missinguser",
            "email": "missing@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "missing@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        "/daily_checkins/999999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404

def test_delete_checkin_requires_authentication(client):
    client.post(
        "/users/register",
        json={
            "username": "noauthuser",
            "email": "noauth@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "noauth@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-28",
            "cycle_day": 6,
            "mood": "Good"
        }
    )

    checkin_id = create_response.json()["id"]

    response = client.delete(
        f"/daily_checkins/{checkin_id}"
    )

    assert response.status_code in [401, 403]

def test_update_own_checkin(client):
    client.post(
        "/users/register",
        json={
            "username": "updateuser",
            "email": "update@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "update@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    # Create the original check-in
    create_response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-29",
            "cycle_day": 7,
            "mood": "Good",
            "energy_level": "Moderate",
            "sleep_quality": "Good"
        }
    )

    assert create_response.status_code == 200

    checkin_id = create_response.json()["id"]

    # Update the check-in
    response = client.put(
        f"/daily_checkins/{checkin_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-29",
            "cycle_day": 7,
            "mood": "Excellent",
            "energy_level": "High",
            "sleep_quality": "Very Good",
            "notes": "Feeling much better today."
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == checkin_id
    assert data["date"] == "2026-09-29"
    assert data["cycle_day"] == 7
    assert data["mood"] == "Excellent"
    assert data["energy_level"] == "High"
    assert data["sleep_quality"] == "Very Good"
    assert data["notes"] == "Feeling much better today."

def test_updated_checkin_persists(client):
    client.post(
        "/users/register",
        json={
            "username": "persistuser",
            "email": "persist@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "persist@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-29",
            "cycle_day": 7,
            "mood": "Bad"
        }
    )

    checkin_id = create_response.json()["id"]

    client.put(
        f"/daily_checkins/{checkin_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-29",
            "cycle_day": 7,
            "mood": "Good"
        }
    )

    # Retrieve check-ins
    response = client.get(
        "/daily_checkins/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == checkin_id
    assert data[0]["mood"] == "Good"

def test_user_cannot_update_another_users_checkin(client):
    # First user
    client.post(
        "/users/register",
        json={
            "username": "firstupdate",
            "email": "firstupdate@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "firstupdate@example.com",
            "password": "password123"
        }
    )

    first_token = login_response.json()["access_token"]

    # First user's check-in
    create_response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {first_token}"},
        json={
            "date": "2026-09-29",
            "cycle_day": 7,
            "mood": "Good"
        }
    )

    checkin_id = create_response.json()["id"]

    # Second user
    client.post(
        "/users/register",
        json={
            "username": "secondupdate",
            "email": "secondupdate@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "secondupdate@example.com",
            "password": "password123"
        }
    )

    second_token = login_response.json()["access_token"]

    # Second user attempts to update first user's check-in
    response = client.put(
        f"/daily_checkins/{checkin_id}",
        headers={"Authorization": f"Bearer {second_token}"},
        json={
            "date": "2026-09-29",
            "cycle_day": 7,
            "mood": "Excellent"
        }
    )

    assert response.status_code == 404

def test_update_nonexistent_checkin(client):
    client.post(
        "/users/register",
        json={
            "username": "missingupdate",
            "email": "missingupdate@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "missingupdate@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.put(
        "/daily_checkins/999999",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-29",
            "cycle_day": 7,
            "mood": "Good"
        }
    )

    assert response.status_code == 404

def test_update_checkin_requires_authentication(client):
    client.post(
        "/users/register",
        json={
            "username": "noauthupdate",
            "email": "noauthupdate@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "noauthupdate@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    create_response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-09-29",
            "cycle_day": 7,
            "mood": "Good"
        }
    )

    checkin_id = create_response.json()["id"]

    # No Authorization header
    response = client.put(
        f"/daily_checkins/{checkin_id}",
        json={
            "date": "2026-09-29",
            "cycle_day": 7,
            "mood": "Excellent"
        }
    )

    assert response.status_code in [401, 403]

def test_create_period_checkin(client):
    client.post(
        "/users/register",
        json={
            "username": "perioduser",
            "email": "period@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "period@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-10-01",
            "period": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["period"] is True

def test_create_non_period_checkin(client):
    client.post(
        "/users/register",
        json={
            "username": "noperioduser",
            "email": "noperiod@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/users/login",
        data={
            "username": "noperiod@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/daily_checkins/checkin",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "date": "2026-10-01",
            "period": False,
            "bbt": 97.5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["period"] is False


# This test checks the behavior of the cycle day calculation when a user starts a new period. It first registers a user, logs in to obtain a JWT token, and then sends a POST request to the /daily_checkins/checkin endpoint with the token included in the Authorization header to start a period on September 21. The test then verifies that the cycle day is correctly calculated as 1 for that date.
def test_cycle_day_starts_at_one_on_period_start(client, db):
    client.post(
        "/users/register",
        json={
            "username": "cycleuser1",
            "email": "cycle1@example.com",
            "password": "password123"
        }
    )

    token = get_token(client, "cycle1@example.com")

    client.post(
        "/daily_checkins/checkin",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date": "2026-09-21",
            "period": True
        }
    )

    user = db.query(User).filter(
        User.email == "cycle1@example.com"
    ).first()

    assert get_cycle_day(
        db,
        user,
        date(2026, 9, 21)
    ) == 1

# This test checks the behavior of the cycle day calculation when a user does not check in for several days after starting a period. It first registers a user, logs in to obtain a JWT token, and then sends a POST request to the /daily_checkins/checkin endpoint with the token included in the Authorization header to start a period on September 21. The test then verifies that the cycle day continues to increment correctly for September 22, 23, and 24, even though there are no check-ins on those days.
def test_cycle_day_continues_without_checkin(client, db):
    client.post(
        "/users/register",
        json={
            "username": "cycleuser2",
            "email": "cycle2@example.com",
            "password": "password123"
        }
    )

    token = get_token(client, "cycle2@example.com")

    # CD1
    client.post(
        "/daily_checkins/checkin",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date": "2026-09-21",
            "period": True
        }
    )

    user = db.query(User).filter(
        User.email == "cycle2@example.com"
    ).first()

    # No check-ins on Sept 22, 23, or 24.

    assert get_cycle_day(
        db,
        user,
        date(2026, 9, 22)
    ) == 2

    assert get_cycle_day(
        db,
        user,
        date(2026, 9, 23)
    ) == 3

    assert get_cycle_day(
        db,
        user,
        date(2026, 9, 24)
    ) == 4

# This test checks the behavior of the daily check-in endpoint when a user starts a new period, which should reset the cycle day to 1. It first registers a user, logs in to obtain a JWT token, and then sends two POST requests to the /daily_checkins/checkin endpoint with the token included in the Authorization header. The first request starts a period on September 21, and the second request starts a new period on October 19. The test verifies that the cycle day is correctly calculated for dates before and after the new period start.
def test_new_period_starts_new_cycle(client, db):
    client.post(
        "/users/register",
        json={
            "username": "cycleuser3",
            "email": "cycle3@example.com",
            "password": "password123"
        }
    )

    token = get_token(client, "cycle3@example.com")

    # First cycle starts
    client.post(
        "/daily_checkins/checkin",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date": "2026-09-21",
            "period": True
        }
    )

    # New cycle starts
    client.post(
        "/daily_checkins/checkin",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "date": "2026-10-19",
            "period": True
        }
    )

    user = db.query(User).filter(
        User.email == "cycle3@example.com"
    ).first()

    assert get_cycle_day(
        db,
        user,
        date(2026, 10, 18)
    ) == 28

    assert get_cycle_day(
        db,
        user,
        date(2026, 10, 19)
    ) == 1

    assert get_cycle_day(
        db,
        user,
        date(2026, 10, 20)
    ) == 2





