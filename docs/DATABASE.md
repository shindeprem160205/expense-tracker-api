# Database Design

## ER Diagram Description

The database consists of three core entities with clear ownership and referential integrity.

```
┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│      USERS       │         │    CATEGORIES    │         │     EXPENSES     │
├──────────────────┤         ├──────────────────┤         ├──────────────────┤
│ PK  id           │◄───┐    │ PK  id           │◄───┐    │ PK  id           │
│     email (UQ)   │    │    │     name         │    │    │ FK  user_id      │──┐
│     hashed_pass  │    └───►│ FK  user_id      │    └───►│ FK  category_id  │  │
│     full_name    │    1:N  │     created_at   │    1:N  │     title        │  │
│     is_active    │         └──────────────────┘         │     amount       │  │
│     created_at   │◄────────────────────────────────────│     description  │  │
│     updated_at   │              N:1                     │     expense_date │  │
└──────────────────┘                                      │     created_at   │  │
                                                          │     updated_at   │  │
                                                          └──────────────────┘  │
                                                                                │
                                    User owns many Categories and Expenses ◄────┘
```

### Relationships

| Relationship | Cardinality | On Delete |
|-------------|-------------|-----------|
| User → Categories | One-to-Many | CASCADE |
| User → Expenses | One-to-Many | CASCADE |
| Category → Expenses | One-to-Many | RESTRICT |

**CASCADE on user deletion** removes all associated categories and expenses.

**RESTRICT on category deletion** prevents removing a category that still has expenses (data integrity).

## PostgreSQL Schema

See [`schema.sql`](./schema.sql) for the executable DDL.

### Table: `users`

| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| email | VARCHAR(255) | NOT NULL, UNIQUE |
| hashed_password | VARCHAR(255) | NOT NULL |
| full_name | VARCHAR(255) | NOT NULL |
| is_active | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() |

### Table: `categories`

| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(100) | NOT NULL |
| user_id | INTEGER | FK → users(id), ON DELETE CASCADE |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |
| — | — | UNIQUE(user_id, name) |

### Table: `expenses`

| Column | Type | Constraints |
|--------|------|-------------|
| id | SERIAL | PRIMARY KEY |
| user_id | INTEGER | FK → users(id), ON DELETE CASCADE |
| category_id | INTEGER | FK → categories(id), ON DELETE RESTRICT |
| title | VARCHAR(200) | NOT NULL |
| amount | NUMERIC(12,2) | NOT NULL, CHECK (amount > 0) |
| description | TEXT | NULLABLE |
| expense_date | DATE | NOT NULL |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() |

## Default Categories

On user registration, eight default categories are seeded:

`Food`, `Transport`, `Shopping`, `Bills`, `Entertainment`, `Healthcare`, `Education`, `Other`

## Indexing Strategy

- `users.email` — fast login lookups
- `categories.user_id` — list categories per user
- `expenses.user_id` — filter expenses per user
- `expenses.expense_date` — date-range analytics queries
- `expenses.category_id` — category-wise joins

## Sample Analytics Queries

**Monthly total for a user:**
```sql
SELECT
    EXTRACT(YEAR FROM expense_date) AS year,
    EXTRACT(MONTH FROM expense_date) AS month,
    SUM(amount) AS total_amount,
    COUNT(*) AS expense_count
FROM expenses
WHERE user_id = :user_id
GROUP BY year, month
ORDER BY year, month;
```

**Category-wise spending:**
```sql
SELECT
    c.id,
    c.name,
    COALESCE(SUM(e.amount), 0) AS total_amount,
    COUNT(e.id) AS expense_count
FROM categories c
LEFT JOIN expenses e ON e.category_id = c.id AND e.user_id = :user_id
WHERE c.user_id = :user_id
GROUP BY c.id, c.name
ORDER BY total_amount DESC;
```
