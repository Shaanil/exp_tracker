import pandas as pd
from src.tracker import db


def add_expense(d, category, amount, note):
    with db.get_conn() as conn:
        conn.execute(
            "INSERT INTO expenses (date, category, amount_cents, note) VALUES (?, ?, ?, ?)",
            (d.isoformat(), category, round(amount * 100), note),
        )
        


def delete_expense(expense_id):
    with db.get_conn() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))


def load_expenses():
    with db.get_conn() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM expenses ORDER BY date DESC, id DESC", conn
        )
    df["amount"] = df["amount_cents"] / 100
    return df


def set_budget(category, amount):
    with db.get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO budgets (category, amount_cents) VALUES (?, ?)",
            (category, round(amount * 100)),
        )


def load_budgets():
    with db.get_conn() as conn:
        rows = conn.execute("SELECT category, amount_cents FROM budgets").fetchall()
    return {category: cents / 100 for category, cents in rows}