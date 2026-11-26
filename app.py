from datetime import date

import pandas as pd
import streamlit as st

from src.tracker import services

st.title("💸 Expense Tracker")

# ---------- Sidebar: set monthly budgets ----------
saved_budgets = services.load_budgets()
with st.sidebar.form("budgets_form"):
    st.header("Monthly budgets")
    new_budgets = {
        cat: st.number_input(
            cat, min_value=0.0, step=10.0, value=saved_budgets.get(cat, 0.0)
        )
        for cat in services.CATEGORIES
    }
    if st.form_submit_button("Save budgets"):
        for cat, value in new_budgets.items():
            services.set_budget(cat, value)
        st.success("Budgets saved!")

budgets = services.load_budgets()

# ---------- Add expense ----------
with st.form("add_expense", clear_on_submit=True):
    d = st.date_input("Date", date.today())
    category = st.selectbox("Category", services.CATEGORIES)
    amount = st.number_input("Amount", min_value=0.0, step=1.0)
    note = st.text_input("Note (optional)")
    if st.form_submit_button("Add expense") and amount > 0:
        services.add_expense(d, category, amount, note)
        st.success("Added!")

# ---------- Load data ----------
df = services.load_expenses()
today = date.today()

if df.empty:
    this_month = df
    st.info("No expenses yet. Add your first one above.")
else:
    df["date"] = pd.to_datetime(df["date"])
    this_month = df[
        (df["date"].dt.month == today.month) & (df["date"].dt.year == today.year)
    ]

# ---------- This month ----------
st.subheader("This month")
total_budget = services.total_budget()
st.metric(
    "Total spent",
    f"{this_month['amount'].sum():,.2f}",
    delta=f"of {total_budget:,.2f} budgeted" if total_budget > 0 else None,
    delta_color="off",
)

spent_category = {}
for cat in services.CATEGORIES:
    spent = services.spent_by_category(cat)
    spent_category.update({cat: spent})
    budget = services.budget_by_category(cat)
    ratio = services.spent_ratio(spent, budget)

    st.write(f"**{cat}**: {spent:,.2f} / {budget:,.2f}")
    st.progress(min(ratio, 1.0))
    if ratio > 1:
        st.error(f"Over budget by {spent - budget:,.2f}")
    elif ratio >= 0.8:
        st.warning(f"You've used {ratio:.0%} of this budget")

if not this_month.empty:
    st.bar_chart(spent_category)

# ---------- All expenses + delete ----------
if not df.empty:
    st.subheader("All expenses")
    st.dataframe(df[["date", "category", "amount", "note"]])

    with st.expander("Delete an expense"):
        options = {
            f"{r.date:%Y-%m-%d} | {r.category} | {r.amount:,.2f} | {r.note or ''}": r.id
            for r in df.itertuples()
        }
        choice = st.selectbox("Pick one", list(options.keys()))
        if st.button("Delete"):
            services.delete_expense(options[choice])
            st.rerun()
