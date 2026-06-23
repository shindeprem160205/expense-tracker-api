# Project Structure — File by File Explanation

Complete guide to every file: what it does, what technology it uses, and how the code works.

---

## Folder Tree

```
expense-tracker-api/
│
├── app/                          # Main application
│   ├── main.py                   # Entry point — starts FastAPI
│   ├── config.py                 # Settings from .env
│   ├── database.py               # DB connection
│   ├── dependencies.py           # JWT auth helper
│   │
│   ├── models/                   # Database tables (SQLAlchemy)
│   │   ├── user.py
│   │   ├── category.py
│   │   └── expense.py
│   │
│   ├── schemas/                  # API input/output (Pydantic)
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── expense.py
│   │   └── analytics.py
│   │
│   ├── routers/                  # HTTP endpoints (FastAPI)
│   │   ├── auth.py
│   │   ├── expenses.py
│   │   ├── categories.py
│   │   └── analytics.py
│   │
│   ├── services/                   # Business logic
│   │   ├── auth_service.py
│   │   ├── expense_service.py
│   │   ├── category_service.py
│   │   └── analytics_service.py
│   │
│   ├── utils/
│   │   └── security.py           # JWT + password hashing
│   │
│   └── static/                     # Web UI for users
│       ├── index.html
│       ├── app.css
│       └── app.js
│
├── tests/                          # pytest tests
├── docs/                           # Documentation
├── requirements.txt
├── run.ps1                         # Windows startup script
├── Dockerfile
└── docker-compose.yml
```

---

## How a Request Flows

```
Browser → main.py → router → service → model → database
                              ↓
                         JSON response
```

---

## Root Files

| File | Technology | Purpose |
|------|------------|---------|
| `requirements.txt` | pip | FastAPI, SQLAlchemy, JWT, bcrypt |
| `requirements-dev.txt` | pip | pytest, httpx for testing |
| `.env.example` | — | Config template (copy to `.env`) |
| `.gitignore` | Git | Excludes `.env`, `.venv`, `*.db` |
| `run.ps1` | PowerShell | Start app + open browser |
| `pytest.ini` | pytest | Test configuration |
| `Dockerfile` | Docker | Container image for API |
| `docker-compose.yml` | Docker | API + PostgreSQL together |
| `README.md` | Markdown | GitHub homepage documentation |

---

## `app/main.py` — Entry Point

**Technology:** FastAPI, Uvicorn

**What it does:**
- Creates the FastAPI application
- Creates database tables on startup
- Registers all API routes under `/api/v1`
- Serves web UI at `/`
- Enables CORS and Swagger at `/docs`

```python
@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)  # Create tables if missing
    yield

app.include_router(auth_router, prefix="/api/v1")
app.include_router(expenses_router, prefix="/api/v1")

@app.get("/")
def home():
    return FileResponse("index.html")  # User-friendly web app
```

---

## `app/config.py` — Configuration

**Technology:** Pydantic Settings

Loads settings from `.env` file:

```python
class Settings(BaseSettings):
    database_url: str      # sqlite or postgresql URL
    secret_key: str        # JWT signing key
    access_token_expire_minutes: int = 30
```

---

## `app/database.py` — Database Connection

**Technology:** SQLAlchemy 2.0

```python
engine = create_engine(database_url)           # Connection pool
SessionLocal = sessionmaker(bind=engine)     # Session factory

def get_db():
    db = SessionLocal()
    try:
        yield db      # One session per HTTP request
    finally:
        db.close()    # Always cleanup
```

- **SQLite** for local dev (`expense_tracker.db`)
- **PostgreSQL** for Docker/production

---

## `app/dependencies.py` — Authentication Guard

**Technology:** FastAPI Depends, OAuth2 Bearer

```python
def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    user_id = decode_access_token(token)     # Read JWT
    user = db.get(User, int(user_id))        # Load user
    if not user:
        raise HTTPException(401)             # Block request
    return user
```

Used on every protected route:
```python
def list_expenses(current_user: User = Depends(get_current_user)):
    ...
```

---

## `app/models/` — Database Tables

**Technology:** SQLAlchemy ORM

### `user.py` — Users table
```python
class User(Base):
    email: str              # Unique login
    hashed_password: str    # bcrypt hash — never plain text
    full_name: str
    expenses: relationship  # One user → many expenses
```

### `category.py` — Categories table
```python
class Category(Base):
    name: str               # e.g. "Food", "Transport"
    user_id: int            # Each user has own categories
```

### `expense.py` — Expenses table
```python
class Expense(Base):
    title: str
    amount: Decimal         # NUMERIC(12,2) in PostgreSQL
    expense_date: date
    user_id: int            # Owner
    category_id: int        # Which category
```

**Relationships:**
```
User ──< Category ──< Expense
User ──< Expense
```

---

## `app/schemas/` — API Validation

**Technology:** Pydantic v2

| Schema | Used for |
|--------|----------|
| `UserCreate` | Register request body |
| `UserResponse` | User JSON (no password) |
| `ExpenseCreate` | Create expense body |
| `ExpenseUpdate` | Partial update |
| `Token` | Login response `{ access_token }` |

```python
class ExpenseCreate(BaseModel):
    title: str
    amount: Decimal = Field(gt=0)    # Must be > 0
    category_id: int
    expense_date: date
```

**Models vs Schemas:**
- **Model** = database structure
- **Schema** = API contract (validates JSON, hides secrets)

---

## `app/services/` — Business Logic

### `auth_service.py`
| Method | What it does |
|--------|--------------|
| `register_user` | Hash password, create user, seed 8 categories |
| `authenticate_user` | Verify email + password |
| `create_token_for_user` | Issue JWT |

### `expense_service.py`
| Method | What it does |
|--------|--------------|
| `create_expense` | Validate category belongs to user, save |
| `list_expenses` | Filter by user_id, date, category |
| `update_expense` | Partial update |
| `delete_expense` | Remove if owned by user |

**Security rule:** Every query includes `user_id == current_user.id`

### `analytics_service.py`
| Method | SQL concept |
|--------|-------------|
| `monthly_summary` | `GROUP BY year, month, SUM(amount)` |
| `category_spending` | `JOIN` + percentage calculation |
| `total_expenses` | `SUM(amount), COUNT(*)` |

### `category_service.py`
| Method | What it does |
|--------|--------------|
| `list_categories` | User's categories only |
| `create_category` | Prevent duplicate names |

---

## `app/routers/` — HTTP Endpoints

Thin layer — receives HTTP, calls service, returns JSON.

### `auth.py`
| Endpoint | Auth | Action |
|----------|------|--------|
| `POST /auth/register` | No | Sign up |
| `POST /auth/login` | No | Get JWT |
| `GET /auth/me` | Yes | Profile |

### `expenses.py`
| Endpoint | Action |
|----------|--------|
| `POST /expenses` | Create |
| `GET /expenses` | List (filter by date/category) |
| `GET /expenses/{id}` | Get one |
| `PUT /expenses/{id}` | Update |
| `DELETE /expenses/{id}` | Delete |

### `categories.py`
| Endpoint | Action |
|----------|--------|
| `GET /categories` | List |
| `POST /categories` | Create |

### `analytics.py`
| Endpoint | Action |
|----------|--------|
| `GET /analytics/monthly-summary` | Per-month totals |
| `GET /analytics/category-spending` | By category + % |
| `GET /analytics/total` | Grand total |

---

## `app/utils/security.py` — JWT & Passwords

**Technology:** bcrypt, python-jose

```python
# Password hashing (one-way)
get_password_hash("mypassword")  → "$2b$12$abc..."
verify_password("mypassword", hash)  → True/False

# JWT tokens
create_access_token(user_id)  → "eyJhbGciOiJIUzI1NiIs..."
decode_access_token(token)    → user_id or None
```

**JWT payload:**
```json
{ "sub": "1", "exp": 1719142800 }
```

---

## `app/static/` — Web UI

**Technology:** HTML, CSS, JavaScript (no npm/React)

| File | Purpose |
|------|---------|
| `index.html` | Login page, expense form, dashboard layout |
| `app.css` | Styling (cards, buttons, colors) |
| `app.js` | Calls API, stores JWT in localStorage |

```javascript
// Login → store token
localStorage.setItem("token", access_token);

// Protected API call
fetch("/api/v1/expenses", {
  headers: { "Authorization": "Bearer " + token }
});
```

**Why:** Normal users use http://localhost:8000 — not Swagger.

---

## `tests/` — Automated Tests

**Technology:** pytest, FastAPI TestClient

| File | Tests |
|------|-------|
| `conftest.py` | Shared fixtures (client, auth token) |
| `test_auth.py` | Register, login, 401 |
| `test_expenses.py` | CRUD |
| `test_categories.py` | Defaults, duplicates |
| `test_analytics.py` | Totals, summaries |
| `test_health.py` | Health check |

```bash
pytest -v    # 17 tests
```

Uses in-memory SQLite — no PostgreSQL needed for tests.

---

## Technology Map

```
┌─────────────────────────────────────────────────────┐
│  Uvicorn          Runs the server                   │
│  FastAPI          API framework + Swagger           │
│  Pydantic         Validates JSON                    │
│  SQLAlchemy       Talks to database                 │
│  SQLite/PostgreSQL Stores data                      │
│  bcrypt           Hashes passwords                  │
│  python-jose      Creates/reads JWT                 │
│  pytest           Runs tests                        │
│  Docker           Packages for deployment             │
│  HTML/CSS/JS      User web interface                │
└─────────────────────────────────────────────────────┘
```

---

## Example: User Adds an Expense

```
1. User types "Lunch ₹50" in web form (static/app.js)
2. JS sends POST /api/v1/expenses + Bearer token
3. expenses.py router receives request
4. dependencies.py validates JWT → gets User
5. Pydantic validates ExpenseCreate schema
6. ExpenseService.create_expense() saves to DB
7. JSON response returned
8. JS refreshes expense list on screen
```

---

## Interview One-Liner

> "Layered FastAPI REST API — routers handle HTTP, services contain business logic, SQLAlchemy ORM maps to PostgreSQL, JWT+bcrypt for auth, user-scoped queries for security, analytics via SQL aggregations, web UI for end users, 17 pytest tests, Docker-ready."
