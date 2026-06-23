const API = "/api/v1";

let token = localStorage.getItem("token");

// ── Helpers ──────────────────────────────────────────────

function show(el) { el.classList.remove("hidden"); }
function hide(el) { el.classList.add("hidden"); }

function formatMoney(amount) {
  return "₹" + parseFloat(amount).toLocaleString("en-IN", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function formatDate(dateStr) {
  return new Date(dateStr + "T00:00:00").toLocaleDateString("en-IN", {
    day: "numeric", month: "short", year: "numeric",
  });
}

function showError(msg) {
  const el = document.getElementById("auth-error");
  el.textContent = msg;
  show(el);
}

async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (options.body && typeof options.body === "object" && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(options.body);
  }
  const res = await fetch(API + path, { ...options, headers });
  if (res.status === 401) { logout(); throw new Error("Session expired. Please login again."); }
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || "Something went wrong");
  return data;
}

// ── Auth ─────────────────────────────────────────────────

function showAuth() {
  show(document.getElementById("auth-screen"));
  hide(document.getElementById("main-screen"));
}

function showApp() {
  hide(document.getElementById("auth-screen"));
  show(document.getElementById("main-screen"));
}

function logout() {
  token = null;
  localStorage.removeItem("token");
  showAuth();
}

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");
    const isLogin = tab.dataset.tab === "login";
    hide(document.getElementById(isLogin ? "register-form" : "login-form"));
    show(document.getElementById(isLogin ? "login-form" : "register-form"));
    hide(document.getElementById("auth-error"));
  });
});

document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  hide(document.getElementById("auth-error"));
  try {
    const form = new FormData();
    form.append("username", document.getElementById("login-email").value);
    form.append("password", document.getElementById("login-password").value);
    const data = await fetch(API + "/auth/login", { method: "POST", body: form })
      .then((r) => r.json());
    if (!data.access_token) throw new Error(data.detail || "Login failed");
    token = data.access_token;
    localStorage.setItem("token", token);
    await loadApp();
  } catch (err) {
    showError(err.message || "Wrong email or password");
  }
});

document.getElementById("register-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  hide(document.getElementById("auth-error"));
  try {
    await api("/auth/register", {
      method: "POST",
      body: {
        email: document.getElementById("register-email").value,
        password: document.getElementById("register-password").value,
        full_name: document.getElementById("register-name").value,
      },
    });
    // Auto-login after register
    const form = new FormData();
    form.append("username", document.getElementById("register-email").value);
    form.append("password", document.getElementById("register-password").value);
    const data = await fetch(API + "/auth/login", { method: "POST", body: form }).then((r) => r.json());
    token = data.access_token;
    localStorage.setItem("token", token);
    await loadApp();
  } catch (err) {
    showError(typeof err.message === "string" ? err.message : "Could not create account");
  }
});

document.getElementById("logout-btn").addEventListener("click", logout);
document.getElementById("refresh-btn").addEventListener("click", loadDashboard);

// ── Dashboard ────────────────────────────────────────────

let categories = [];

async function loadApp() {
  const user = await api("/auth/me");
  document.getElementById("user-greeting").textContent = `Hi, ${user.full_name.split(" ")[0]}!`;
  showApp();

  categories = await api("/categories");
  const select = document.getElementById("expense-category");
  select.innerHTML = categories.map((c) => `<option value="${c.id}">${c.name}</option>`).join("");

  document.getElementById("expense-date").value = new Date().toISOString().split("T")[0];

  await loadDashboard();
}

async function loadDashboard() {
  const [expenses, total, spending] = await Promise.all([
    api("/expenses"),
    api("/analytics/total"),
    api("/analytics/category-spending"),
  ]);

  document.getElementById("total-amount").textContent = formatMoney(total.total_amount);
  document.getElementById("total-count").textContent = total.expense_count;

  const top = spending.find((s) => parseFloat(s.total_amount) > 0);
  document.getElementById("top-category").textContent = top ? top.category_name : "—";

  renderCategories(spending);
  renderExpenses(expenses);
}

function renderCategories(spending) {
  const container = document.getElementById("category-chart");
  const active = spending.filter((s) => parseFloat(s.total_amount) > 0);
  if (!active.length) {
    container.innerHTML = '<p class="empty">Add expenses to see breakdown</p>';
    return;
  }
  const max = Math.max(...active.map((s) => parseFloat(s.total_amount)));
  container.innerHTML = active.map((s) => {
    const pct = (parseFloat(s.total_amount) / max) * 100;
    return `
      <div class="category-item">
        <span class="category-name">${s.category_name}</span>
        <span class="category-amount">${formatMoney(s.total_amount)}</span>
        <div class="category-bar-bg"><div class="category-bar" style="width:${pct}%"></div></div>
      </div>`;
  }).join("");
}

function renderExpenses(expenses) {
  const container = document.getElementById("expense-list");
  if (!expenses.length) {
    container.innerHTML = '<p class="empty">No expenses yet. Add your first one above!</p>';
    return;
  }
  container.innerHTML = expenses.map((e) => `
    <div class="expense-item">
      <div class="expense-info">
        <div class="expense-title">${e.title}</div>
        <div class="expense-meta">${e.category.name} · ${formatDate(e.expense_date)}</div>
      </div>
      <span class="expense-amount">${formatMoney(e.amount)}</span>
      <button class="btn btn-danger" onclick="deleteExpense(${e.id})">Delete</button>
    </div>
  `).join("");
}

async function deleteExpense(id) {
  if (!confirm("Delete this expense?")) return;
  await api(`/expenses/${id}`, { method: "DELETE" });
  await loadDashboard();
}

document.getElementById("expense-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const msg = document.getElementById("expense-msg");
  hide(msg);
  try {
    await api("/expenses", {
      method: "POST",
      body: {
        title: document.getElementById("expense-title").value,
        amount: document.getElementById("expense-amount").value,
        category_id: parseInt(document.getElementById("expense-category").value),
        description: document.getElementById("expense-notes").value || null,
        expense_date: document.getElementById("expense-date").value,
      },
    });
    document.getElementById("expense-form").reset();
    document.getElementById("expense-date").value = new Date().toISOString().split("T")[0];
    msg.textContent = "Expense added!";
    show(msg);
    setTimeout(() => hide(msg), 2500);
    await loadDashboard();
  } catch (err) {
    alert(err.message);
  }
});

// ── Boot ─────────────────────────────────────────────────

if (token) {
  loadApp().catch(() => logout());
} else {
  showAuth();
}
