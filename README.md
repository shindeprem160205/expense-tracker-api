# Expense Tracker API

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00)](https://sqlalchemy.org)
[![pytest](https://img.shields.io/badge/Tests-pytest-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A full-stack **Expense Tracker** application with a REST API backend and a built-in web interface. Track daily spending, organize expenses by category, and view analytics — all from your browser.

Built with **FastAPI**, **SQLAlchemy**, **JWT authentication**, and **pytest**. Suitable as a portfolio project for backend and full-stack roles.

**Live repository:** [github.com/shindeprem160205/expense-tracker-api](https://github.com/shindeprem160205/expense-tracker-api)

---

## Overview

| Layer | Description |
|-------|-------------|
| **Web App** | User-friendly UI at `http://localhost:8000` — sign up, add expenses, view totals |
| **REST API** | Versioned endpoints under `/api/v1` with JWT protection |
| **Database** | SQLite for local development · PostgreSQL for Docker/production |
| **Documentation** | Auto-generated Swagger UI at `/docs` |

---

## Features

- **Authentication** — User registration, login, JWT tokens, bcrypt password hashing
- **Expense Management** — Create, read, update, delete expenses with categories and date filters
- **Analytics** — Monthly summaries, category-wise spending breakdown, grand totals
- **Web Interface** — Clean browser UI — no Postman or Swagger required for end users
- **API Documentation** — Interactive OpenAPI docs (Swagger UI + ReDoc)
- **Testing** — 17 integration tests with pytest
- **Docker Ready** — Optional Docker Compose setup with PostgreSQL

---

## How to Run

Choose the method that fits your setup. **Method 1 is recommended** for Windows users with no Docker installed.

---

### Method 1 — One-Click Start (Windows, Recommended)

**Requirements:** Python 3.12+ installed

```powershell
git clone https://github.com/shindeprem160205/expense-tracker-api.git
cd expense-tracker-api
.\run.ps1
```

The script will:
1. Create a virtual environment (first run only)
2. Install dependencies
3. Create `.env` from template (first run only)
4. Free port 8000 if an old server is running
5. Open your browser automatically

**Open the app:** [http://localhost:8000](http://localhost:8000)

> **Stop the server:** Press `Ctrl+C` in the terminal.

---

### Method 2 — Manual Setup (Windows / macOS / Linux)

**Requirements:** Python 3.12+

```powershell
# 1. Clone the repository
git clone https://github.com/shindeprem160205/expense-tracker-api.git
cd expense-tracker-api

# 2. Create and activate virtual environment
python -m venv .venv

# Windows
.\.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements-dev.txt

# 4. Configure environment
copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux

# 5. Start the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Open the app:** [http://localhost:8000](http://localhost:8000)

| URL | Purpose |
|-----|---------|
| [http://localhost:8000](http://localhost:8000) | Web application (for users) |
| [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger API documentation (for developers) |
| [http://localhost:8000/health](http://localhost:8000/health) | Health check endpoint |

---

### Method 3 — Docker (PostgreSQL + API)

**Requirements:** [Docker Desktop](https://docs.docker.com/desktop/) installed and running

```powershell
git clone https://github.com/shindeprem160205/expense-tracker-api.git
cd expense-tracker-api
copy .env.example .env
```

Update `.env` for PostgreSQL:

```env
DATABASE_URL=postgresql://expense_user:expense_pass@localhost:5432/expense_tracker
```

Start services:

```powershell
docker compose up --build -d
```

| Service | URL |
|---------|-----|
| Web App | [http://localhost:8000](http://localhost:8000) |
| API Docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| PostgreSQL | `localhost:5432` |

Stop services:

```powershell
docker compose down
```

---

### Method 4 — Run Tests

```powershell
# Activate virtual environment first, then:
pip install -r requirements-dev.txt
pytest -v
```

With coverage report:

```powershell
pytest --cov=app --cov-report=term-missing
```

---

## Using the Application

### Web Interface (Recommended)

1. Open [http://localhost:8000](http://localhost:8000)
2. Click **Sign up** and create an account
3. Log in with your email and password
4. Add expenses using the form on the dashboard
5. View totals, category breakdown, and recent transactions

No API knowledge required.

### API (Developers)

1. Open [http://localhost:8000/docs](http://localhost:8000/docs)
2. Register via `POST /api/v1/auth/register`
3. Click **Authorize** and log in with your credentials
4. Test endpoints interactively

---

## Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12 | Core language |
| FastAPI | 0.115 | Web framework & OpenAPI docs |
| Uvicorn | 0.32 | ASGI server |
| SQLAlchemy | 2.0 | ORM & database abstraction |
| Pydantic | v2 | Request/response validation |
| SQLite | — | Local development database |
| PostgreSQL | 16 | Production database (Docker) |
| python-jose | 3.3 | JWT token handling |
| bcrypt | 4.2 | Password hashing |
| pytest | 8.3 | Integration testing |
| Docker | — | Containerized deployment |

---

## Project Structure

```
expense-tracker-api/
├── app/
│   ├── main.py              # Application entry point
│   ├── config.py            # Environment-based settings
│   ├── database.py          # Database engine & sessions
│   ├── dependencies.py      # JWT authentication dependency
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── routers/             # API route handlers
│   ├── services/            # Business logic layer
│   ├── utils/security.py    # JWT & password utilities
│   └── static/              # Web UI (HTML, CSS, JavaScript)
├── tests/                   # pytest integration tests
├── docs/                    # Technical documentation
├── run.ps1                  # Windows one-click launcher
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── requirements-dev.txt
```

**Detailed file-by-file explanation:** [docs/PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md)

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/health` | Service health check | No |
| `POST` | `/api/v1/auth/register` | Register a new user | No |
| `POST` | `/api/v1/auth/login` | Login and receive JWT | No |
| `GET` | `/api/v1/auth/me` | Get current user profile | Yes |
| `GET` | `/api/v1/categories` | List user categories | Yes |
| `POST` | `/api/v1/categories` | Create a category | Yes |
| `POST` | `/api/v1/expenses` | Create an expense | Yes |
| `GET` | `/api/v1/expenses` | List expenses (filterable) | Yes |
| `GET` | `/api/v1/expenses/{id}` | Get a single expense | Yes |
| `PUT` | `/api/v1/expenses/{id}` | Update an expense | Yes |
| `DELETE` | `/api/v1/expenses/{id}` | Delete an expense | Yes |
| `GET` | `/api/v1/analytics/monthly-summary` | Monthly spending totals | Yes |
| `GET` | `/api/v1/analytics/category-spending` | Spending by category | Yes |
| `GET` | `/api/v1/analytics/total` | Grand total & count | Yes |

Full reference: [docs/API.md](docs/API.md)

---

## Architecture

```
Browser (Web UI / API Client)
         │
         ▼
   FastAPI Routers        ← HTTP layer, input validation
         │
         ▼
   Services               ← Business logic
         │
         ▼
   SQLAlchemy ORM          ← Data access
         │
         ▼
   SQLite / PostgreSQL     ← Persistence
```

- **Layered design** — Routers → Services → ORM for separation of concerns
- **JWT authentication** — Stateless bearer tokens on all protected routes
- **User-scoped data** — Every query filters by `user_id` for data isolation
- **Auto OpenAPI** — Swagger UI generated from Pydantic schemas

Details: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) · [docs/AUTH_FLOW.md](docs/AUTH_FLOW.md)

---

## Environment Variables

Copy `.env.example` to `.env` and adjust as needed:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./expense_tracker.db` | Database connection string |
| `SECRET_KEY` | — | JWT signing secret (change in production) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token expiration time |
| `CORS_ORIGINS` | `http://localhost:3000,...` | Allowed CORS origins |
| `DEBUG` | `false` | Enable debug mode |

> Never commit `.env` to version control. It is listed in `.gitignore`.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `docker: not recognized` | Use **Method 1** or **Method 2** — Docker is optional |
| Port 8000 already in use | Run `.\run.ps1` (auto-fixes) or stop old server with `Ctrl+C` |
| `{"detail":"Not Found"}` on `/` | Restart the server after pulling latest code |
| `Repository not found` on push | Set correct remote: `git remote set-url origin https://github.com/shindeprem160205/expense-tracker-api.git` |

---

## Documentation

| Document | Description |
|----------|-------------|
| [PROJECT_STRUCTURE.md](docs/PROJECT_STRUCTURE.md) | File-by-file code walkthrough |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design & request lifecycle |
| [DATABASE.md](docs/DATABASE.md) | ER diagram & PostgreSQL schema |
| [API.md](docs/API.md) | Complete endpoint reference |
| [AUTH_FLOW.md](docs/AUTH_FLOW.md) | JWT authentication workflow |
| [SECURITY.md](docs/SECURITY.md) | Security practices |
| [TESTING.md](docs/TESTING.md) | Testing strategy |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Cloud & Docker deployment |
| [INTERVIEW_QA.md](docs/INTERVIEW_QA.md) | Interview questions & answers |

---

## Resume Description

> **Expense Tracker API** — Python, FastAPI, SQLAlchemy, JWT, PostgreSQL, Docker  
> Designed and built a full-stack expense management application with a REST API and web interface. Implemented JWT authentication with bcrypt, layered architecture (routers → services → ORM), user-scoped data isolation, SQL-based analytics, Docker deployment, and 17 pytest integration tests.  
> **GitHub:** [github.com/shindeprem160205/expense-tracker-api](https://github.com/shindeprem160205/expense-tracker-api)

---

## Author

**Prem Shinde** — [github.com/shindeprem160205](https://github.com/shindeprem160205)

---

