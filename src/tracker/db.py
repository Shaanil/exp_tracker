import sqlite3

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


init_db()
