# Authentication Flow

## Flow Diagram

```
┌────────┐                              ┌─────────────┐                              ┌──────────┐
│ Client │                              │  FastAPI    │                              │PostgreSQL│
└───┬────┘                              └──────┬──────┘                              └────┬─────┘
    │                                          │                                          │
    │  POST /auth/register                     │                                          │
    │  { email, password, full_name }          │                                          │
    │─────────────────────────────────────────►│                                          │
    │                                          │  Hash password (bcrypt)                  │
    │                                          │  Insert user + default categories        │
    │                                          │─────────────────────────────────────────►│
    │                                          │◄─────────────────────────────────────────│
    │◄─────────────────────────────────────────│  201 UserResponse                        │
    │                                          │                                          │
    │  POST /auth/login                        │                                          │
    │  username=email&password=***             │                                          │
    │─────────────────────────────────────────►│                                          │
    │                                          │  Lookup user by email                    │
    │                                          │─────────────────────────────────────────►│
    │                                          │◄─────────────────────────────────────────│
    │                                          │  Verify bcrypt hash                      │
    │                                          │  Create JWT (sub=user_id, exp=30min)     │
    │◄─────────────────────────────────────────│  200 { access_token, token_type }        │
    │                                          │                                          │
    │  GET /expenses                           │                                          │
    │  Authorization: Bearer <JWT>             │                                          │
    │─────────────────────────────────────────►│                                          │
    │                                          │  Decode JWT → extract user_id            │
    │                                          │  Load user from DB                       │
    │                                          │─────────────────────────────────────────►│
    │                                          │◄─────────────────────────────────────────│
    │                                          │  Execute protected business logic        │
    │◄─────────────────────────────────────────│  200 Response                            │
    │                                          │                                          │
```

## JWT Workflow Explanation

### 1. Token Creation (Login)

When a user logs in successfully:

1. `AuthService.authenticate_user()` verifies email and bcrypt-hashed password.
2. `create_access_token(subject=str(user.id))` builds a JWT payload:
   ```json
   {
     "sub": "1",
     "exp": 1719142800
   }
   ```
3. The token is signed with `HS256` using `SECRET_KEY` from environment variables.
4. Client stores the token (memory, secure storage) and sends it on subsequent requests.

### 2. Token Validation (Protected Routes)

On every protected endpoint:

1. `OAuth2PasswordBearer` extracts the token from the `Authorization: Bearer` header.
2. `decode_access_token()` verifies signature and expiration using `python-jose`.
3. `sub` claim is parsed as `user_id`.
4. User is loaded from PostgreSQL; inactive users are rejected.
5. If any step fails → `401 Unauthorized` with `WWW-Authenticate: Bearer`.

### 3. Why Stateless JWT?

| Benefit | Explanation |
|---------|-------------|
| Scalability | No server-side session store; any API instance can validate tokens |
| Mobile-friendly | Works well for SPAs and mobile apps |
| Decoupled | Auth service can be extracted to a separate microservice later |

### 4. Security Notes

- Tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30).
- Passwords are **never** stored in plain text — only bcrypt hashes.
- Use HTTPS in production to prevent token interception.
- Rotate `SECRET_KEY` periodically in production deployments.

### 5. Swagger UI Authorization

1. Open `http://localhost:8000/docs`
2. Click **Authorize**
3. Enter email as **username** and password
4. Swagger attaches the Bearer token to protected endpoints automatically
