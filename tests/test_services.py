from datetime import date

import pytest

import src.tracker.db
from src.tracker.services import (
    add_expense,
    load_expenses,
    spent_by_category,
    spent_ratio,
    delete_expense,
    spent_this_month,
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
    assert spent_ratio(spent=1000, budget=0) == 0 # Considered as Infinity Budget

def test_spent_by_category():
    
    add_expense (d,"Food",550,"Test Food")
    add_expense (d,"Food",650,"Test Food")
    add_expense (d,"Food",750,"Test Food")
    add_expense (d,"Bills",850,"Test Bills")

    assert spent_by_category("Bills") == 850.00
    assert spent_by_category("Food") == 1950.00


def test_delete_expense():
    add_expense (d,"Food",550,"isRemaining")
    add_expense (d,"Food",650,"isDeleted")

    _id=int(load_expenses().iloc[0]["id"])
    delete_expense (_id)
    assert load_expenses().iloc[0]["id"] != "isDeleted"

def test_spent_this_month():
    _d=d.fromisocalendar(2026,44,1)
    add_expense (d,"Food",550,"X Month")
    add_expense (d,"Food",650,"X Month")
    add_expense (_d,"Food",550,"Y Month")
    add_expense (_d,"Food",650,"Y Month")

    x= spent_this_month().groupby("category")["amount"].sum()
    assert x["Food"] == 1200