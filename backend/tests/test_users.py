
# This is a test file for the user registration endpoint of the FastAPI application. 
# It uses pytest and the TestClient from FastAPI to simulate requests to the API.

# The test_register_user function sends a POST request to the /users/register endpoint with a JSON payload containing a username, email, and password. It then checks that the response status code is 200 (indicating success) and verifies that the returned data matches the input values.
def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


# This test checks the behavior of the user registration endpoint when attempting to register a user with an email that already exists in the database. It first registers a user and expects a successful response (status code 200). Then, it attempts to register the same user again and expects a failure response (status code 400), indicating that duplicate registrations are not allowed.
def test_register_duplicate_user(client):
    user = {
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "password123"
    }

    # First registration should succeed
    response = client.post("/users/register", json=user)

    assert response.status_code == 200

    # Second registration should fail
    response = client.post("/users/register", json=user)

    assert response.status_code == 400

# This test checks the user login functionality. It first registers a user and then attempts to log in using the registered email and password. The test verifies that the login is successful (status code 200) and that the response contains an access token and the correct token type.
def test_login_user(client):
    # Register the user first
    client.post(
        "/users/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123"
        }
    )

    # Login using OAuth2 form data
    response = client.post(
        "/users/login",
        data={
            "username": "login@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


# This test checks the behavior of the user login endpoint when attempting to log in with an incorrect password. It first registers a user and then attempts to log in using the correct email but an incorrect password. The test verifies that the login attempt fails (status code 401), indicating that the provided credentials are invalid.
def test_login_wrong_password(client):
    # Register the user
    client.post(
        "/users/register",
        json={
            "username": "wrongpassuser",
            "email": "wrongpass@example.com",
            "password": "password123"
        }
    )

    # Attempt login with the wrong password
    response = client.post(
        "/users/login",
        data={
            "username": "wrongpass@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 400

def test_login_nonexistent_user(client):
    response = client.post(
        "/users/login",
        data={
            "username": "doesnotexist@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 400