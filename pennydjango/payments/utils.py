def get_amount_plus_fee(amount):
    total_paid = (amount+0.30)/(1-0.029)
    total_paid = round(total_paid, 2)
    return total_paid
