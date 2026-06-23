from datetime import date


def _get_food_category_id(client, auth_headers) -> int:
    categories = client.get("/api/v1/categories", headers=auth_headers).json()
    return next(c["id"] for c in categories if c["name"] == "Food")


def test_create_expense(client, auth_headers):
    category_id = _get_food_category_id(client, auth_headers)
    response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "Lunch",
            "amount": "15.50",
            "category_id": category_id,
            "description": "Office lunch",
            "expense_date": str(date.today()),
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Lunch"
    assert data["category"]["name"] == "Food"


def test_list_expenses(client, auth_headers):
    category_id = _get_food_category_id(client, auth_headers)
    client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "Coffee",
            "amount": "4.00",
            "category_id": category_id,
            "expense_date": str(date.today()),
        },
    )
    response = client.get("/api/v1/expenses", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_expense(client, auth_headers):
    category_id = _get_food_category_id(client, auth_headers)
    create_response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "Dinner",
            "amount": "25.00",
            "category_id": category_id,
            "expense_date": str(date.today()),
        },
    )
    expense_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/expenses/{expense_id}",
        headers=auth_headers,
        json={"title": "Updated Dinner", "amount": "30.00"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Dinner"


def test_delete_expense(client, auth_headers):
    category_id = _get_food_category_id(client, auth_headers)
    create_response = client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": "Snack",
            "amount": "3.00",
            "category_id": category_id,
            "expense_date": str(date.today()),
        },
    )
    expense_id = create_response.json()["id"]

    delete_response = client.delete(f"/api/v1/expenses/{expense_id}", headers=auth_headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/v1/expenses/{expense_id}", headers=auth_headers)
    assert get_response.status_code == 404
