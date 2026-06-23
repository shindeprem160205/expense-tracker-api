def test_list_default_categories(client, auth_headers):
    response = client.get("/api/v1/categories", headers=auth_headers)
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) >= 8
    assert any(c["name"] == "Food" for c in categories)


def test_create_category(client, auth_headers):
    response = client.post(
        "/api/v1/categories",
        headers=auth_headers,
        json={"name": "Travel"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Travel"


def test_create_duplicate_category(client, auth_headers):
    client.post("/api/v1/categories", headers=auth_headers, json={"name": "Travel"})
    response = client.post(
        "/api/v1/categories",
        headers=auth_headers,
        json={"name": "Travel"},
    )
    assert response.status_code == 400
