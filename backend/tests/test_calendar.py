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