from datetime import date


def _create_expense(client, auth_headers, title: str, amount: str, category_name: str = "Food"):
    categories = client.get("/api/v1/categories", headers=auth_headers).json()
    category_id = next(c["id"] for c in categories if c["name"] == category_name)
    client.post(
        "/api/v1/expenses",
        headers=auth_headers,
        json={
            "title": title,
            "amount": amount,
            "category_id": category_id,
            "expense_date": str(date.today()),
        },
    )


def test_total_expenses(client, auth_headers):
    _create_expense(client, auth_headers, "Groceries", "50.00")
    _create_expense(client, auth_headers, "Bus", "5.00", "Transport")

    response = client.get("/api/v1/analytics/total", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert float(data["total_amount"]) >= 55.0
    assert data["expense_count"] >= 2


def test_monthly_summary(client, auth_headers):
    _create_expense(client, auth_headers, "Rent", "1000.00", "Bills")

    response = client.get("/api/v1/analytics/monthly-summary", headers=auth_headers)
    assert response.status_code == 200
    summary = response.json()
    assert len(summary) >= 1
    assert float(summary[0]["total_amount"]) >= 1000.0


def test_category_spending(client, auth_headers):
    _create_expense(client, auth_headers, "Pizza", "20.00")
    _create_expense(client, auth_headers, "Taxi", "15.00", "Transport")

    response = client.get("/api/v1/analytics/category-spending", headers=auth_headers)
    assert response.status_code == 200
    spending = response.json()
    assert any(item["category_name"] == "Food" for item in spending)
    assert any(float(item["total_amount"]) > 0 for item in spending)
