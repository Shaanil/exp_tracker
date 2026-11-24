import sqlite3
import pandas as pd

DB = "data/expenses.db"

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


init_db()



def add_expense(d, category, amount, note):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO expenses (date, category, amount_cents, note) VALUES (?, ?, ?, ?)",
            (d.isoformat(), category, round(amount * 100), note),
        )


def delete_expense(expense_id):
    with get_conn() as conn:
        conn.execute(
            "DELETE FROM expenses WHERE id = ?", (expense_id,))


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