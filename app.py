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


def add_expense(d, category, amount, note):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO expenses (date, category, amount_cents, note) VALUES (?, ?, ?, ?)",
            (d.isoformat(), category, round(amount * 100), note),
        )


def load_expenses():
    with get_conn() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM expenses ORDER BY date DESC, id DESC", conn
        )
    df["amount"] = df["amount_cents"] / 100
    return df


init_db()
st.title("💸 Expense Tracker")

with st.form("add_expense", clear_on_submit=True):
    d = st.date_input("Date", date.today())
    category = st.selectbox("Category", CATEGORIES)
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    note = st.text_input("Note (optional)")
    if st.form_submit_button("Add expense") and amount > 0:
        add_expense(d, category, amount, note)
        st.success("Added!")

df = load_expenses()
if df.empty:
    st.info("No expenses yet. Add your first one above.")
else:
    df["date"] = pd.to_datetime(df["date"])
    today = date.today()
    this_month = df[
        (df["date"].dt.month == today.month) & (df["date"].dt.year == today.year)
    ]

    st.subheader("This month")
    st.metric("Total spent", f"{this_month['amount'].sum():,.2f}")
    st.bar_chart(this_month.groupby("category")["amount"].sum())

    st.subheader("All expenses")
    st.dataframe(df[["date", "category", "amount", "note"]])
