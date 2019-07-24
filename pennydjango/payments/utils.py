from decimal import Decimal
from math import ceil

from django.conf import settings


def get_amount_plus_fee(amount):
    assert isinstance(amount, Decimal)
    # Stripes charges 2.9%, that is STRIPE_FEE
    total_paid = amount + (amount * settings.STRIPE_FEE)
    # Plus 30 cents that is STRIPE_FIXED_FEE
    total_paid += settings.STRIPE_FIXED_FEE
    total_paid = ceil(total_paid * Decimal(100))
    return total_paid
