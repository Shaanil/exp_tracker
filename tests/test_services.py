import os
from datetime import date

import src.tracker.db
from src.tracker.services import (
    add_expense,
    load_expenses,
    spent_ratio,
)
_testDB = 'tests/test_expenses.db'

# Test: Verify Test
def test_app_function (monkeypatch):
    #Testing Database
    _testDB = 'tests/test_expenses.db'

    
    # Override the constant or environment variable directly inside the test
    monkeypatch.setattr(src.tracker.db, "DB", str(_testDB))
    # Or: monkeypatch.setenv("DATABASE_URL", f"sqlite:///{fake_db}")
    
    src.tracker.db.init_db()
    assert os.path.exists(_testDB)



# Test: Adding to DB
def test_add_expense(monkeypatch):

    d = date.today()
    category = "Bills"
    amount = 500
    note = "Test"

    monkeypatch.setattr(src.tracker.db, "DB", str(_testDB))
    add_expense(d, category, amount, note)
    last_row = load_expenses().iloc[0]
    assert last_row["category"] == "Bills"
    assert last_row["amount"] == 500


# Test: Ratio Output
def test_spent_ratio():

    assert spent_ratio(spent=1000, budget=1500) < 1
    assert spent_ratio(spent=1500, budget=1000) > 1
    assert spent_ratio(spent=1000, budget=1000) == 1

