from decimal import Decimal
from math import ceil

from django.conf import settings
from django.db.models import Sum

from leases.models import MoveInCost
from leases.constants import LEASE_STATUS
from payments.models import Transaction


def get_amount_plus_fee(amount):
    assert isinstance(amount, Decimal)
    # Stripes charges 2.9%, that is STRIPE_FEE
    total_paid = amount + (amount * settings.STRIPE_FEE)
    # Plus 30 cents that is STRIPE_FIXED_FEE
    total_paid += settings.STRIPE_FIXED_FEE
    total_paid = ceil(total_paid * Decimal(100))
    return total_paid

def get_lease_total_pending(lease):
    lease_total_paid = Transaction.objects.filter(
        lease_member__offer=lease
    ).aggregate(Sum('amount'))
    lease_move_in_costs = MoveInCost.objects.total_by_offer(lease.id)
    lease_total_pending = lease_move_in_costs
    if lease_total_paid['amount__sum'] is not None:
        total_sum = lease_total_paid['amount__sum']
        lease_total_pending = lease_move_in_costs - total_sum
    return lease_total_pending

def update_lesase_status(lease):
    lease.status = LEASE_STATUS[1][0]
    lease.save()
