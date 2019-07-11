from django.db import models

from penny.models import BaseModel, User
from leases.models import Lease, LeaseMember
from payments.constants import PAYMENT_METHOD, FROM_TO


class Transaction(BaseModel):
    lease_member = models.ForeignKey(LeaseMember, on_delete=models.SET_NULL, null=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='entered_by_transaction', null=True)
    transaction_user =  models.ForeignKey(User, on_delete=models.SET_NULL, related_name='transaction_user', null=True)
    token = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    from_to = models.CharField(max_length=155, choices=FROM_TO, default=FROM_TO[0])
    payment_method = models.CharField(max_length=155, choices=PAYMENT_METHOD, default=PAYMENT_METHOD[0])
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    @classmethod
    def get_lease_transactions(cls, lease):
        transaction = cls.objects.filter(service=lease)
        
        return transaction
