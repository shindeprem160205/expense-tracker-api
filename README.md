# Expense Tracker REST API

A production-quality **Expense Tracker REST API** built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **JWT authentication** — designed as a portfolio project for software engineering freshers.

[Python](https://python.org)
[FastAPI](https://fastapi.tiangolo.com)
[PostgreSQL](https://postgresql.org)
[Docker](https://docker.com)

---

## Features

- **User Authentication** — Register, login, JWT tokens, bcrypt password hashing
- **Expense Management** — Full CRUD with categories, date filtering, pagination
- **Analytics** — Monthly summary, category-wise spending, total expenses
- **API Documentation** — Auto-generated Swagger UI and OpenAPI spec
- **Docker Support** — One-command deployment with PostgreSQL
- **Test Suite** — pytest with 20+ integration tests

---

## Quick Start (Windows — easiest)

```powershell
git clone https://github.com/yourusername/expense-tracker-api.git
cd expense-tracker-api
.\run.ps1
```

Open **http://localhost:8000** — use the web app (no Swagger needed).

📁 **File-by-file code explanation:** [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)  
🐙 **Push to GitHub:** [docs/GITHUB_SETUP.md](docs/GITHUB_SETUP.md)

---

## Quick Start (Docker)

```bash
git clone https://github.com/yourusername/expense-tracker-api.git
cd expense-tracker-api
cp .env.example .env
docker compose up --build -d
```

Open **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Tech Stack


| Technology       | Purpose             |
| ---------------- | ------------------- |
| Python 3.12      | Core language       |
| FastAPI          | Web framework       |
| PostgreSQL 16    | Relational database |
| SQLAlchemy 2.0   | ORM                 |
| Pydantic v2      | Data validation     |
| python-jose      | JWT tokens          |
| passlib + bcrypt | Password hashing    |
| Docker           | Containerization    |
| pytest           | Testing             |


---

## Project Architecture

```
Client → FastAPI Routers → Services → SQLAlchemy ORM → PostgreSQL
```

Detailed architecture: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

### Folder Structure

```
expense-tracker-api/
├── app/
│   ├── main.py                 # Application entry point
│   ├── config.py               # Settings
│   ├── database.py             # DB engine & session
│   ├── dependencies.py         # Auth dependency
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── routers/                # API routes
│   ├── services/               # Business logic
│   └── utils/security.py       # JWT & hashing
├── tests/                      # pytest suite
├── docs/                       # Technical documentation
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Database Design

### ER Diagram

```
USERS (1) ──────< CATEGORIES (1) ──────< EXPENSES
  │                                          ▲
  └──────────────────────────────────────────┘
              (User owns Expenses directly)
```


| Entity         | Key Fields                                        |
| -------------- | ------------------------------------------------- |
| **users**      | email, hashed_password, full_name                 |
| **categories** | name, user_id (unique per user)                   |
| **expenses**   | title, amount, expense_date, category_id, user_id |


Full schema: [docs/DATABASE.md](docs/DATABASE.md) | [docs/schema.sql](docs/schema.sql)

---

## API Endpoints


| Method | Endpoint                              | Description     | Auth |
| ------ | ------------------------------------- | --------------- | ---- |
| GET    | `/health`                             | Health check    | No   |
| POST   | `/api/v1/auth/register`               | Register user   | No   |
| POST   | `/api/v1/auth/login`                  | Get JWT token   | No   |
| GET    | `/api/v1/auth/me`                     | Current user    | Yes  |
| GET    | `/api/v1/categories`                  | List categories | Yes  |
| POST   | `/api/v1/categories`                  | Create category | Yes  |
| POST   | `/api/v1/expenses`                    | Create expense  | Yes  |
| GET    | `/api/v1/expenses`                    | List expenses   | Yes  |
| GET    | `/api/v1/expenses/{id}`               | Get expense     | Yes  |
| PUT    | `/api/v1/expenses/{id}`               | Update expense  | Yes  |
| DELETE | `/api/v1/expenses/{id}`               | Delete expense  | Yes  |
| GET    | `/api/v1/analytics/monthly-summary`   | Monthly totals  | Yes  |
| GET    | `/api/v1/analytics/category-spending` | By category     | Yes  |
| GET    | `/api/v1/analytics/total`             | Grand total     | Yes  |


Full API docs: [docs/API.md](docs/API.md)

---

## Authentication Flow

```
Register → Login → Receive JWT → Send Bearer token on protected routes
```

Detailed flow: [docs/AUTH_FLOW.md](docs/AUTH_FLOW.md)

### JWT Workflow

1. User logs in with email + password
2. Server validates credentials (bcrypt)
3. Server issues signed JWT (`sub=user_id`, `exp=30min`)
4. Client sends `Authorization: Bearer <token>` on each request
5. Server decodes JWT, loads user, executes request

---

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```

---

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest -v
pytest --cov=app --cov-report=term-missing
```

Testing guide: [docs/TESTING.md](docs/TESTING.md)

---

## Docker Configuration

```yaml
# docker-compose.yml runs:
# - postgres:16-alpine (port 5432)
# - FastAPI API (port 8000)
```

Deployment guide: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## Security Best Practices

- bcrypt password hashing
- JWT with expiration
- User-scoped data access
- Pydantic input validation
- Environment-based secrets
- CORS configuration
- SQL injection prevention via ORM

Full guide: [docs/SECURITY.md](docs/SECURITY.md)

---

## Why This Tech Stack?

### Why FastAPI?

Modern Python framework with automatic OpenAPI docs, Pydantic validation, high performance, and minimal boilerplate. Industry adoption is growing rapidly for microservices and APIs.

### Why PostgreSQL?

ACID-compliant, production-proven relational database. Excellent for transactional data and analytics queries (GROUP BY, date functions). Foreign keys enforce data integrity.

### Why JWT?

Stateless authentication scales horizontally. No server-side session store needed. Standard for REST APIs consumed by SPAs and mobile apps.

### Why SQLAlchemy?

Python's most mature ORM. Type-safe 2.0 syntax, connection pooling, relationship management, and database portability between SQLite (tests) and PostgreSQL (production).

### Why Docker?

Consistent dev/prod environments. One command to run API + database. Demonstrates DevOps awareness expected in modern backend roles.

### Why Swagger?

FastAPI auto-generates interactive API documentation. Enables testing without Postman. Shows API design competency to interviewers.

---

## Resume-Ready Project Description

> **Expense Tracker REST API** — Python, FastAPI, PostgreSQL, SQLAlchemy, JWT, Docker
>
> Designed and built a production-ready REST API for personal expense management with user authentication, CRUD operations, and spending analytics. Implemented JWT-based auth with bcrypt password hashing, layered architecture (routers → services → ORM), and user-scoped data isolation. Integrated PostgreSQL with optimized indexes for analytics queries (monthly summaries, category-wise spending). Containerized with Docker Compose, documented with auto-generated Swagger/OpenAPI, and achieved full test coverage with pytest integration tests.

---

## GitHub README Section (Copy-Paste)

```markdown
## 🏗️ Expense Tracker API

Backend REST API for tracking personal expenses with analytics.

**Stack:** Python · FastAPI · PostgreSQL · SQLAlchemy · JWT · Docker · pytest

### Highlights
- JWT authentication with bcrypt password hashing
- Full expense CRUD with category management
- Analytics: monthly summary, category breakdown, totals
- Auto-generated Swagger/OpenAPI documentation
- Docker Compose for one-command setup
- 20+ pytest integration tests

### Run locally
docker compose up --build -d
# → http://localhost:8000/docs
```

---

## Interview Preparation

Common questions with detailed answers: [docs/INTERVIEW_QA.md](docs/INTERVIEW_QA.md)

---

## Documentation Index


| Document                                | Description                             |
| --------------------------------------- | --------------------------------------- |
| [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | File-by-file code explanation |
| [GITHUB_SETUP.md](docs/GITHUB_SETUP.md) | Push to GitHub guide |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Layered architecture & folder structure |
| [DATABASE.md](docs/DATABASE.md)         | ER diagram & PostgreSQL schema          |
| [API.md](docs/API.md)                   | Endpoint reference                      |
| [AUTH_FLOW.md](docs/AUTH_FLOW.md)       | Authentication & JWT workflow           |
| [SECURITY.md](docs/SECURITY.md)         | Security best practices                 |
| [TESTING.md](docs/TESTING.md)           | pytest strategy                         |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md)     | Docker & cloud deployment               |
| [INTERVIEW_QA.md](docs/INTERVIEW_QA.md) | Interview Q&A                           |


---

## License

MIT