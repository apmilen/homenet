from django.db import models
from django.urls import reverse

from penny.models import BaseModel, User
from listings.models import Listing
from leases.constants import LEASE_STATUS, DEFAULT_LEASE_STATUS


class Lease(BaseModel):
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # gross_rent = models.DecimalField(max_digits=15, decimal_places=2)
    # net_effective_rent = models.DecimalField(max_digits=15, decimal_places=2)
    offer = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="What would they like to pay?"
    )
    length_of_lease = models.PositiveSmallIntegerField(help_text='In months')
    move_in_date = models.DateField()
    op = models.PositiveSmallIntegerField(verbose_name='OP%')
    total_broker_fee = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=50,
        choices=LEASE_STATUS,
        default=DEFAULT_LEASE_STATUS
    )

    def detail_link(self):
        return reverse('leases:detail', args=[self.id])
