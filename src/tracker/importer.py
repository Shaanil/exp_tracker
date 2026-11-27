def phrase_amount(amount):
    try:
        amount = float(amount.replace(",", ""))
        phrase_amount = amount * 100
        if phrase_amount % 1 != 0 or (phrase_amount < 0):
            return ValueError
        else:
            return phrase_amount
    except ValueError:
        return ValueError
