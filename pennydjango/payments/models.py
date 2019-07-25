from django.db import models

from penny.models import BaseModel, User
from leases.models import LeaseMember
from payments.constants import PAYMENT_METHOD, FROM_TO, CLIENT_TO_APP, DEFAULT_PAYMENT_METHOD


class Transaction(BaseModel):
    lease_member = models.ForeignKey(
        LeaseMember,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    entered_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='entered_by_transaction',
        null=True,
        blank=True
    )
    transaction_user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        related_name='transaction_user',
        null=True,
        blank=True
    )
    token = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    from_to = models.CharField(
        max_length=64,
        choices=FROM_TO,
        default=CLIENT_TO_APP)
    payment_method = models.CharField(
        max_length=32,
        choices=PAYMENT_METHOD,
        default=DEFAULT_PAYMENT_METHOD
    )
    stripe_charge_id = modles.CharField(
        max_length=100, 
        unique=True, 
        null=True, 
        blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
