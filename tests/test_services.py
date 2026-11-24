from src.tracker.services import load_expenses,add_expense,spent_ratio
from datetime import date


#Test: Adding to DB 
def test_add_expense ():
   

    d=date.today()
    category="Bills"
    amount=500
    note= "Test"

    add_expense(d,category,amount,note)
    last_row=load_expenses().iloc[0]
    assert last_row["category"]=="Bills"
    assert last_row["amount"] == 500


#Test: Ratio Output

def test_spent_ratio():

    assert spent_ratio(spent=1000,budget=1500)  < 1
    assert spent_ratio(spent=1500, budget=1000) > 1
    assert spent_ratio(spent=1000,budget=1000) == 1 