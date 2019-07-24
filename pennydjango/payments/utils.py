from decimal import Decimal
from math import ceil


def get_amount_plus_fee(amount):
    stripe_fixed_comission = Decimal(0.30)
    total_paid = (amount+stripe_fixed_comission)/Decimal(1-0.029)
    total_paid = ceil(total_paid)
    return total_paid
