# Project Architecture

## Overview

The Expense Tracker API follows a **layered architecture** optimized for clarity, testability, and portfolio demonstration. Each layer has a single responsibility and communicates through well-defined interfaces.

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (Browser / App)                  │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTP/JSON
┌─────────────────────────────▼───────────────────────────────┐
│  Presentation Layer — FastAPI Routers                       │
│  auth.py | expenses.py | categories.py | analytics.py       │
└─────────────────────────────┬───────────────────────────────┘
                              │ Pydantic Schemas
┌─────────────────────────────▼───────────────────────────────┐
│  Business Logic Layer — Services                            │
│  AuthService | ExpenseService | CategoryService | Analytics │
└─────────────────────────────┬───────────────────────────────┘
                              │ SQLAlchemy ORM
┌─────────────────────────────▼───────────────────────────────┐
│  Data Access Layer — Models + Database Session              │
│  User | Category | Expense                                  │
└─────────────────────────────┬───────────────────────────────┘
                              │ SQL
┌─────────────────────────────▼───────────────────────────────┐
│  PostgreSQL Database                                        │
└─────────────────────────────────────────────────────────────┘
```

## Design Principles

| Principle | Implementation |
|-----------|----------------|
| Separation of Concerns | Routers handle HTTP; services contain business rules |
| Dependency Injection | FastAPI `Depends()` for DB sessions and auth |
| Type Safety | Pydantic v2 schemas + SQLAlchemy 2.0 typed mappings |
| Security by Default | JWT auth on all protected routes; bcrypt password hashing |
| Stateless API | JWT tokens; no server-side sessions |

## Folder Structure

```
expense-tracker-api/
├── app/
│   ├── main.py              # FastAPI app factory, middleware, lifespan
│   ├── config.py            # Environment-based settings (Pydantic Settings)
│   ├── database.py          # SQLAlchemy engine, session, Base
│   ├── dependencies.py      # Auth dependency (get_current_user)
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── category.py
│   │   └── expense.py
│   ├── schemas/             # Request/response Pydantic models
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── expense.py
│   │   └── analytics.py
│   ├── routers/             # API route handlers
│   │   ├── auth.py
│   │   ├── expenses.py
│   │   ├── categories.py
│   │   └── analytics.py
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   ├── expense_service.py
│   │   ├── category_service.py
│   │   └── analytics_service.py
│   └── utils/
│       └── security.py      # JWT + password hashing
├── tests/                   # pytest test suite
├── docs/                    # Technical documentation
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Request Lifecycle

1. Client sends HTTP request with optional `Authorization: Bearer <token>` header.
2. FastAPI router receives request and validates input via Pydantic schema.
3. `get_current_user` dependency decodes JWT and loads user from DB (protected routes).
4. Service layer executes business logic and database queries.
5. ORM models are converted to response schemas and returned as JSON.

## Scalability Considerations

- **Connection pooling** configured on SQLAlchemy engine (`pool_size=10`, `max_overflow=20`).
- **Stateless design** allows horizontal scaling behind a load balancer.
- **Indexed columns** on `user_id`, `expense_date`, and `email` for query performance.
- Future extensions: Redis caching, Alembic migrations, background jobs (Celery), rate limiting.
