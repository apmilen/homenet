from decimal import Decimal
from math import ceil

from django.conf import settings


def get_amount_plus_fee(amount):
    total_paid = (amount + settings.STRIPE_FEE)/Decimal(1-0.029)
    total_paid = ceil(total_paid * 100)
    return total_paid
