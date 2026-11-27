from src.tracker.importer import phrase_amount

def test_phrase_amount():
    assert phrase_amount("12.50") == 1250
    assert phrase_amount("0.10") == 10
    assert phrase_amount("1,200.00") == 120000
    assert phrase_amount("") == ValueError
    assert phrase_amount("abc") == ValueError
    assert phrase_amount("12.345") == ValueError
    assert phrase_amount("-5") == ValueError