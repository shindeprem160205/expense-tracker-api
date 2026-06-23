# Testing Strategy

## Framework

- **pytest** — test runner and fixtures
- **httpx TestClient** — synchronous HTTP testing against FastAPI
- **SQLite in-memory** — fast, isolated test database (no PostgreSQL required for CI)

## Test Structure

```
tests/
├── conftest.py          # Shared fixtures (client, auth_headers, DB setup)
├── test_auth.py         # Register, login, /me
├── test_categories.py   # List and create categories
├── test_expenses.py     # CRUD operations
├── test_analytics.py    # Summary endpoints
└── test_health.py       # Health check
```

## Fixtures

| Fixture | Purpose |
|---------|---------|
| `setup_database` | Creates/drops tables before each test (autouse) |
| `db_session` | Provides SQLAlchemy session |
| `client` | FastAPI TestClient with DB override |
| `auth_headers` | Pre-authenticated Bearer token headers |

## Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Verbose with coverage
pytest -v --cov=app --cov-report=term-missing
```

## What We Test

| Area | Coverage |
|------|----------|
| Auth | Registration, duplicate email, login, invalid credentials, protected route |
| Categories | Default seeding, create, duplicate prevention |
| Expenses | Create, list, update, delete, 404 handling |
| Analytics | Total, monthly summary, category spending |
| Health | Liveness endpoint |

## Testing Principles

1. **Isolation** — each test gets a fresh in-memory database
2. **Real HTTP** — TestClient exercises full request/response cycle
3. **Auth flow** — tests use actual register → login → Bearer token pattern
4. **No mocks for DB** — integration-style tests against real SQLAlchemy + SQLite

## CI Integration (GitHub Actions example)

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements-dev.txt
      - run: pytest -v --cov=app
```

## Future Test Enhancements

- Property-based testing with `hypothesis`
- PostgreSQL integration tests via `testcontainers`
- Load testing with `locust`
- Contract testing against OpenAPI spec
