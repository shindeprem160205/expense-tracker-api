# Deployment Guide

## Option 1: Docker Compose (Recommended)

### Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- Git

### Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/expense-tracker-api.git
cd expense-tracker-api

# Copy environment file and set a secure secret
cp .env.example .env
# Edit .env — change SECRET_KEY to a long random string

# Start PostgreSQL + API
docker compose up --build -d

# Verify
curl http://localhost:8000/health
```

**Access:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- PostgreSQL: `localhost:5432` (user: `expense_user`, db: `expense_tracker`)

### Stop Services

```bash
docker compose down        # Stop containers
docker compose down -v     # Stop and remove volumes (deletes DB data)
```

---

## Option 2: Local Development (without Docker)

### Prerequisites

- Python 3.12+
- PostgreSQL 16+

### Steps

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Create database
psql -U postgres -c "CREATE USER expense_user WITH PASSWORD 'expense_pass';"
psql -U postgres -c "CREATE DATABASE expense_tracker OWNER expense_user;"

# Configure environment
cp .env.example .env

# Run API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Option 3: Cloud Deployment

### Render / Railway / Fly.io

1. Push code to GitHub
2. Create a **PostgreSQL** database service
3. Create a **Web Service** with:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables:
   - `DATABASE_URL` — from managed PostgreSQL
   - `SECRET_KEY` — generate with `openssl rand -hex 32`
   - `CORS_ORIGINS` — your frontend URL

### AWS (ECS + RDS)

1. Build and push Docker image to ECR
2. Provision RDS PostgreSQL instance
3. Deploy ECS Fargate service with environment variables
4. Place Application Load Balancer with HTTPS certificate (ACM)

### Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| DATABASE_URL | Yes | PostgreSQL connection string |
| SECRET_KEY | Yes | JWT signing secret |
| ACCESS_TOKEN_EXPIRE_MINUTES | No | Token TTL (default: 30) |
| CORS_ORIGINS | No | Comma-separated allowed origins |
| DEBUG | No | Enable debug mode (default: false) |

---

## Production Recommendations

- Run behind a reverse proxy (Nginx/Caddy) with TLS termination
- Use managed PostgreSQL with automated backups
- Set `DEBUG=false`
- Configure health check on `/health` for load balancer
- Use `gunicorn` with Uvicorn workers for multi-core:
  ```bash
  gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  ```
