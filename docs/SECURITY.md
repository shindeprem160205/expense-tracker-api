# Security Best Practices

## Implemented in This Project

### Authentication & Authorization

- **JWT Bearer tokens** for stateless authentication
- **bcrypt** password hashing (adaptive cost factor)
- **User scoping**: all expense/category queries filter by `user_id` — users cannot access others' data
- **Inactive user check** on token validation

### Input Validation

- **Pydantic v2** validates all request bodies and query parameters
- Email format validation via `EmailStr`
- Amount must be `> 0` with 2 decimal places
- Password minimum length: 8 characters

### Database Security

- Parameterized queries via SQLAlchemy ORM (prevents SQL injection)
- Foreign key constraints enforce referential integrity
- `ON DELETE CASCADE` for user-owned data cleanup
- `ON DELETE RESTRICT` prevents orphaned expense references

### Configuration

- Secrets loaded from environment variables (`.env`), never hardcoded
- `.env` excluded from git via `.gitignore`
- `SECRET_KEY` must be changed in production

### API Hardening

- CORS configured via environment (restrict origins in production)
- Connection pool with `pool_pre_ping` for stale connection recovery
- Structured HTTP error responses (no stack traces in production)

## Production Checklist

- [ ] Set a strong, random `SECRET_KEY` (32+ bytes)
- [ ] Enable HTTPS/TLS (reverse proxy: Nginx, Caddy, or cloud load balancer)
- [ ] Restrict `CORS_ORIGINS` to your frontend domain only
- [ ] Use managed PostgreSQL with encrypted connections (`sslmode=require`)
- [ ] Set `DEBUG=false`
- [ ] Implement rate limiting (e.g., `slowapi` or API gateway)
- [ ] Add request logging and monitoring (Prometheus, Sentry)
- [ ] Regular dependency updates (`pip-audit`, Dependabot)
- [ ] Database backups and point-in-time recovery
- [ ] Consider refresh tokens for long-lived sessions

## OWASP API Security Alignment

| Risk | Mitigation |
|------|------------|
| Broken Authentication | JWT + bcrypt, token expiration |
| Broken Object Level Authorization | user_id filtering on all queries |
| Mass Assignment | Pydantic schemas with explicit fields |
| Security Misconfiguration | Environment-based config, no debug in prod |
| Injection | ORM parameterized queries |
