import sqlite3
from datetime import date

import pandas as pd
import streamlit as st

DB = "expenses.db"
CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Fun", "Other"]


def get_conn():
    return sqlite3.connect(DB)


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                category TEXT NOT NULL,
                amount_cents INTEGER NOT NULL,
                note TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                category TEXT PRIMARY KEY,
                amount_cents INTEGER NOT NULL
            )
        """)


def add_expense(d, category, amount, note):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO expenses (date, category, amount_cents, note) VALUES (?, ?, ?, ?)",
            (d.isoformat(), category, round(amount * 100), note),
        )


def delete_expense(expense_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))


def load_expenses():
    with get_conn() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM expenses ORDER BY date DESC, id DESC", conn
        )
    df["amount"] = df["amount_cents"] / 100
    return df


def set_budget(category, amount):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO budgets (category, amount_cents) VALUES (?, ?)",
            (category, round(amount * 100)),
        )


def load_budgets():
    with get_conn() as conn:
        rows = conn.execute("SELECT category, amount_cents FROM budgets").fetchall()
    return {category: cents / 100 for category, cents in rows}


init_db()
st.title("💸 Expense Tracker")

# ---------- Sidebar: set monthly budgets ----------
saved_budgets = load_budgets()
with st.sidebar.form("budgets_form"):
    st.header("Monthly budgets")
    new_budgets = {
        cat: st.number_input(
            cat, min_value=0.0, step=10.0, value=saved_budgets.get(cat, 0.0)
        )
        for cat in CATEGORIES
    }
    if st.form_submit_button("Save budgets"):
        for cat, value in new_budgets.items():
            set_budget(cat, value)
        st.success("Budgets saved!")

budgets = load_budgets()

# ---------- Add expense ----------
with st.form("add_expense", clear_on_submit=True):
    d = st.date_input("Date", date.today())
    category = st.selectbox("Category", CATEGORIES)
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    note = st.text_input("Note (optional)")
    if st.form_submit_button("Add expense") and amount > 0:
        add_expense(d, category, amount, note)
        st.success("Added!")

# ---------- Load data ----------
df = load_expenses()
today = date.today()

if df.empty:
    this_month = df
    st.info("No expenses yet. Add your first one above.")
else:
    df["date"] = pd.to_datetime(df["date"])
    this_month = df[
        (df["date"].dt.month == today.month) & (df["date"].dt.year == today.year)
    ]

# ---------- This month ----------
st.subheader("This month")
spent_by_cat = this_month.groupby("category")["amount"].sum()
total_budget = sum(budgets.values())
st.metric(
    "Total spent",
    f"{this_month['amount'].sum():,.2f}",
    delta=f"of {total_budget:,.2f} budgeted" if total_budget > 0 else None,
    delta_color="off",
)

for cat in CATEGORIES:
    budget = budgets.get(cat, 0.0)
    spent = float(spent_by_cat.get(cat, 0.0))
    if budget > 0:
        ratio = spent / budget
        st.write(f"**{cat}**: {spent:,.2f} / {budget:,.2f}")
        st.progress(min(ratio, 1.0))
        if ratio > 1:
            st.error(f"Over budget by {spent - budget:,.2f}")
        elif ratio >= 0.8:
            st.warning(f"You've used {ratio:.0%} of this budget")

if not this_month.empty:
    st.bar_chart(spent_by_cat)

# ---------- All expenses + delete ----------
if not df.empty:
    st.subheader("All expenses")
    st.dataframe(df[["date", "category", "amount", "note"]])

    with st.expander("Delete an expense"):
        options = {
            f"{r.date:%Y-%m-%d} | {r.category} | {r.amount:,.2f} | {r.note or ''}": r.id
            for r in df.itertuples()
        }
        choice = st.selectbox("Pick one", list(options.keys()))
        if st.button("Delete"):
            delete_expense(options[choice])
            st.rerun()  