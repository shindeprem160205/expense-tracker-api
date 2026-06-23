# GitHub Setup Guide

Follow these steps to publish your Expense Tracker project on GitHub.

## Step 1 — Create a GitHub account (if needed)

Go to [https://github.com/signup](https://github.com/signup)

---

## Step 2 — Create a new repository on GitHub

1. Open [https://github.com/new](https://github.com/new)
2. **Repository name:** `expense-tracker-api`
3. **Description:** `Production-ready Expense Tracker REST API with FastAPI, PostgreSQL, JWT, and web UI`
4. Choose **Public** (for portfolio)
5. **Do NOT** check "Add a README" (we already have one)
6. Click **Create repository**

---

## Step 3 — Push your code from PowerShell

```powershell
cd C:\Users\prem\Projects\expense-tracker-api

git add .
git status
git commit -m "Initial commit: Expense Tracker API with FastAPI, JWT, web UI, and tests"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/expense-tracker-api.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## Step 4 — Login when prompted

- **Username:** your GitHub username
- **Password:** use a **Personal Access Token** (not your GitHub password)

Create token: GitHub → Settings → Developer settings → Personal access tokens → Generate (scope: `repo`)

---

## What NOT to upload (already in .gitignore)

- `.env` — secrets
- `.venv/` — virtual environment
- `expense_tracker.db` — local database
