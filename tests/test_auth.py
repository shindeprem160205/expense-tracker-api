def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "alice@example.com",
            "password": "password123",
            "full_name": "Alice Smith",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["full_name"] == "Alice Smith"
    assert "id" in data


def test_register_duplicate_email(client):
    payload = {
        "email": "alice@example.com",
        "password": "password123",
        "full_name": "Alice Smith",
    }
    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "bob@example.com",
            "password": "password123",
            "full_name": "Bob Jones",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "bob@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "nobody@example.com", "password": "wrong"},
    )
    assert response.status_code == 401


def test_get_me_requires_auth(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_get_me_success(client, auth_headers):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
