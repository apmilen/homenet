from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

from leases.models import Lease

from django.conf import settings

import stripe  


class Transaction(models.Model):
    service = models.ForeignKey(Lease, on_delete=models.PROTECT)
    made_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    token = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    aproved = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    @classmethod
    def get_lease_transactions(cls, lease):
        transaction = cls.objects.filter(service=lease)
        
        return transaction

