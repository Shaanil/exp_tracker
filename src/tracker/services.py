import pandas as pd
from src.tracker import db


def add_expense(d, category, amount, note):
    db.add_expense(d, category, amount, note)


def delete_expense(expense_id):
    db.delete_expense(delete_expense)


def load_expenses():
    db.load_expenses()


def set_budget(category, amount):
    db.set_budget(category, amount)


def load_budgets():
    db.load_expenses()

def total_budget():
    return sum(load_budgets().values())

def spent_by_category(category):
    return "work in progress"