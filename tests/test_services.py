from datetime import date

import pytest

import src.tracker.db
from src.tracker.services import (
    add_expense,
    load_expenses,
    spent_by_category,
    spent_ratio,
)

d = date.today()


# Add DB isolation
@pytest.fixture(autouse=True)
def auto_isolate_db (monkeypatch,tmp_path):
    _testDB = tmp_path / "test_expenses.db"
    monkeypatch.setattr(src.tracker.db, "DB", str(_testDB))
    src.tracker.db.init_db()


# Test: Adding to DB
def test_add_expense(monkeypatch):

    category = "Fun"
    amount = 500
    note = "Test"

    add_expense(d, category, amount, note)
    last_row = load_expenses().iloc[0]
    assert last_row["category"] == "Fun"
    assert last_row["amount"] == 500

    


# Test: Ratio Output
def test_spent_ratio():

    assert spent_ratio(spent=1000, budget=1500) < 1
    assert spent_ratio(spent=1500, budget=1000) > 1
    assert spent_ratio(spent=1000, budget=1000) == 1

def test_spent_by_category():
    
    add_expense (d,"Food",550,"Test Food")
    add_expense (d,"Food",650,"Test Food")
    add_expense (d,"Food",750,"Test Food")
    add_expense (d,"Bills",850,"Test Bills")

    assert spent_by_category("Bills") == 850.00
    assert spent_by_category("Food") == 1950.00

