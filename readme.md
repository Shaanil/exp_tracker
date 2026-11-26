# Expense Tracker

A personal expense and budget tracker built with Python, SQLite and Streamlit.

## Features

- [x] Record an expense with amount, date and category
- [x] See how much I spent per category this month
- [x] Get warned when I'm near a budget

## Setup

```bash
git clone https://github.com/Shaanil/exp_tracker.git
cd exp_tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the app

```bash
streamlit run app.py
```

The database is created automatically at `data/expenses.db` on first run.

## Run the tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

## Project structure

- `app.py`: the Streamlit interface
- `src/tracker/db.py`: all SQL lives here
- `src/tracker/services.py`: business logic (totals, budgets)
- `tests/`: pytest tests, which use a temporary database