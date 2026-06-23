# Common Interview Questions & Answers

## General / Architecture

**Q: Walk me through your Expense Tracker API architecture.**

A: It's a layered REST API built with FastAPI. Routers handle HTTP and validation via Pydantic schemas. Services contain business logic. SQLAlchemy ORM models map to PostgreSQL tables. JWT authentication protects all expense and analytics endpoints. Each user's data is isolated by `user_id` filtering.

---

**Q: Why did you separate routers and services?**

A: Separation of concerns. Routers stay thin — they parse HTTP, call services, and return responses. Services are reusable and easier to unit test without HTTP overhead. If we add a CLI or background worker later, services can be called directly.

---

**Q: How do you ensure users can only access their own expenses?**

A: Every expense query includes `Expense.user_id == current_user.id`. The `get_current_user` dependency extracts the user ID from the JWT and loads the user from the database. There's no endpoint that accepts a `user_id` parameter from the client for data access.

---

## FastAPI

**Q: Why FastAPI over Flask or Django REST Framework?**

A: FastAPI provides automatic OpenAPI documentation, native async support, Pydantic validation built-in, and excellent performance (comparable to Node.js/Go). For a portfolio API project, it demonstrates modern Python backend practices with minimal boilerplate.

---

**Q: How does dependency injection work in your project?**

A: FastAPI's `Depends()` injects database sessions and the current user. `get_db()` yields a SQLAlchemy session and closes it after the request. `get_current_user()` decodes the JWT and returns the authenticated user. This keeps route handlers clean and makes testing easy via `app.dependency_overrides`.

---

## PostgreSQL

**Q: Why PostgreSQL instead of SQLite or MongoDB?**

A: PostgreSQL is production-grade with ACID compliance, strong relational integrity via foreign keys, and excellent support for analytics queries (GROUP BY, date extraction). SQLite is great for testing; PostgreSQL is what real companies use for transactional data.

---

**Q: Explain your database relationships.**

A: A User has many Categories and many Expenses (one-to-many). A Category has many Expenses. Deleting a user cascades to their categories and expenses. Deleting a category is restricted if expenses still reference it — preventing data integrity issues.

---

## JWT & Security

**Q: Why JWT instead of session-based authentication?**

A: JWT is stateless — the server doesn't need to store sessions in Redis or memory. Any API instance can validate the token. This scales horizontally and works well for SPAs and mobile clients. Trade-off: tokens can't be revoked easily without a blocklist (acceptable for this scope).

---

**Q: How are passwords stored?**

A: Passwords are hashed with bcrypt. Plain-text passwords are never stored. On login, `verify_password()` compares the submitted password against the stored hash.

---

**Q: What happens when a JWT expires?**

A: `python-jose` raises a `JWTError` during decode. Our `decode_access_token()` returns `None`, and `get_current_user()` raises `401 Unauthorized`. The client must re-authenticate via `/auth/login`.

---

## SQLAlchemy

**Q: Why SQLAlchemy?**

A: SQLAlchemy is the de facto Python ORM. It provides type-safe models (2.0 style with `Mapped`), connection pooling, relationship management, and protection against SQL injection through parameterized queries. It also makes database-agnostic development easier.

---

**Q: What is connection pooling and why did you configure it?**

A: Creating a new database connection per request is expensive. SQLAlchemy's pool maintains reusable connections (`pool_size=10`, `max_overflow=20`). `pool_pre_ping` verifies connections before use, handling stale connections after database restarts.

---

## Docker

**Q: Why Docker?**

A: Docker ensures consistent environments across development, testing, and production. `docker-compose.yml` orchestrates the API and PostgreSQL with a single command. New team members can run the full stack without manual PostgreSQL installation.

---

## Swagger / OpenAPI

**Q: Why Swagger?**

A: FastAPI auto-generates OpenAPI 3.0 documentation from Pydantic schemas and route definitions. Swagger UI at `/docs` lets developers and interviewers interactively test endpoints. It demonstrates API design skills without maintaining separate documentation manually.

---

## Testing

**Q: How do you test authenticated endpoints?**

A: The `auth_headers` fixture registers a user, logs in via OAuth2 form data, extracts the JWT, and returns `Authorization: Bearer <token>` headers. Tests use FastAPI's `TestClient` with an in-memory SQLite database for fast, isolated runs.

---

**Q: Why SQLite for tests but PostgreSQL for production?**

A: SQLite in-memory is fast and requires no external services — ideal for CI pipelines. Production uses PostgreSQL for concurrency, data types (NUMERIC, TIMESTAMPTZ), and feature parity with real deployments. SQLAlchemy abstracts most differences.

---

## Analytics

**Q: How does monthly summary work?**

A: We use SQL `EXTRACT(YEAR/MONTH FROM expense_date)` with `GROUP BY` and `SUM(amount)`. Results are scoped to the authenticated user's expenses. An optional `year` query parameter filters to a specific year.

---

**Q: How do you calculate category percentage?**

A: After aggregating spending per category, we compute `(category_total / grand_total) * 100`, rounded to 2 decimal places. Categories with zero spending show 0%.

---

## Behavioral

**Q: What would you improve if you had more time?**

A: I'd add Alembic migrations, refresh tokens, pagination metadata, rate limiting, structured logging, and PostgreSQL integration tests via testcontainers. I'd also add an expense export endpoint (CSV) and input sanitization middleware.

---

**Q: How would you scale this API to 1 million users?**

A: Horizontal scaling of stateless API instances behind a load balancer, read replicas for analytics queries, Redis caching for frequent summaries, database indexing review, connection pool tuning, and potentially partitioning expenses by date for very large datasets.
