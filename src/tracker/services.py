import pandas as pd
from src.tracker import db
from datetime import date

CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Fun", "Other"]

def add_expense(d, category, amount, note):
    return db.add_expense(d, category, amount, note)


def delete_expense(expense_id):
    return db.delete_expense(expense_id)


def load_expenses():
    return db.load_expenses()


def set_budget(category, amount):
    return db.set_budget(category, amount)


def load_budgets():
    return db.load_budgets()

def total_budget():
    return sum(load_budgets().values())

def spent_by_category(cat):
    spent_by_cat = spent_this_month().groupby("category")["amount"].sum() 
    return (spent_by_cat.get(cat, 0.0))     
     
def budget_by_category(cat):
    return db.load_budgets().get(cat, 0.0)

    
def spent_ratio (budget, spent):
    if budget > 0:
        ratio = spent / budget
    else:
        ratio = 0
    return ratio


def spent_this_month():
        today = date.today()
        df = db.load_expenses()
        df["date"] = pd.to_datetime(df["date"])
        this_month = df[(df['date'].dt.month == today.month) & (df['date'].dt.year == today.year)]    
        return this_month

