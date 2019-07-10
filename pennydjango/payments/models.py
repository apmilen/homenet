from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from penny.models import BaseModel, User
from leases.models import Lease
from payments.constants import PAYMENT_METHOD, FROM_TO


class Transaction(BaseModel):
    service = models.ForeignKey(Lease, on_delete=models.PROTECT, null=True)
    made_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    client_name = models.CharField(max_length=100, null=True)
    token = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    from_to = models.CharField(max_length=155, choices=FROM_TO)
    payment_method = models.CharField(max_length=155, choices=PAYMENT_METHOD)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    @classmethod
    def get_lease_transactions(cls, lease):
        transaction = cls.objects.filter(service=lease)
        
        return transaction
