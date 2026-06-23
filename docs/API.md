# API Endpoint Documentation

Base URL: `http://localhost:8000/api/v1`

Interactive docs: [Swagger UI](http://localhost:8000/docs) | [ReDoc](http://localhost:8000/redoc)

OpenAPI JSON: `http://localhost:8000/openapi.json`

---

## Health

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/health` | No | Service health check |

**Response 200:**
```json
{ "status": "healthy", "service": "Expense Tracker API" }
```

---

## Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/register` | No | Register a new user |
| POST | `/auth/login` | No | Login and receive JWT |
| GET | `/auth/me` | Yes | Get current user profile |

### POST `/auth/register`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "full_name": "Jane Doe"
}
```

**Response 201:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Jane Doe",
  "is_active": true,
  "created_at": "2026-06-23T10:00:00Z"
}
```

### POST `/auth/login`

Uses OAuth2 password flow (`application/x-www-form-urlencoded`).

| Field | Value |
|-------|-------|
| username | User email |
| password | User password |

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

### GET `/auth/me`

**Headers:** `Authorization: Bearer <token>`

---

## Categories

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/categories` | Yes | List user categories |
| POST | `/categories` | Yes | Create a category |

### POST `/categories`

```json
{ "name": "Travel" }
```

---

## Expenses

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/expenses` | Yes | Create expense |
| GET | `/expenses` | Yes | List expenses (filterable) |
| GET | `/expenses/{id}` | Yes | Get single expense |
| PUT | `/expenses/{id}` | Yes | Update expense |
| DELETE | `/expenses/{id}` | Yes | Delete expense |

### POST `/expenses`

```json
{
  "title": "Grocery shopping",
  "amount": "85.50",
  "category_id": 1,
  "description": "Weekly groceries",
  "expense_date": "2026-06-23"
}
```

### GET `/expenses` Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| category_id | int | Filter by category |
| start_date | date | Filter from date (YYYY-MM-DD) |
| end_date | date | Filter to date |
| skip | int | Pagination offset (default 0) |
| limit | int | Page size (default 100, max 500) |

---

## Analytics

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/analytics/monthly-summary` | Yes | Monthly spending totals |
| GET | `/analytics/category-spending` | Yes | Spending by category |
| GET | `/analytics/total` | Yes | Overall expense total |

### GET `/analytics/monthly-summary`

| Parameter | Type | Description |
|-----------|------|-------------|
| year | int | Optional year filter |

**Response:**
```json
[
  {
    "year": 2026,
    "month": 6,
    "total_amount": "1250.75",
    "expense_count": 18
  }
]
```

### GET `/analytics/category-spending`

| Parameter | Type | Description |
|-----------|------|-------------|
| start_date | date | Optional start filter |
| end_date | date | Optional end filter |

**Response:**
```json
[
  {
    "category_id": 1,
    "category_name": "Food",
    "total_amount": "450.00",
    "expense_count": 12,
    "percentage": "36.00"
  }
]
```

### GET `/analytics/total`

**Response:**
```json
{
  "total_amount": "1250.75",
  "expense_count": 18,
  "start_date": null,
  "end_date": null
}
```

---

## Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Validation error or business rule violation |
| 401 | Missing or invalid JWT token |
| 404 | Resource not found |
| 422 | Request body/query validation failed |

**Example:**
```json
{ "detail": "Expense not found" }
```
