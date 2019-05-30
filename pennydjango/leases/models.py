from django.db import models

from penny.models import BaseModel

from listings.models import Listing


class Lease(BaseModel):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    # gross_rent = models.DecimalField(max_digits=15, decimal_places=2)
    # net_effective_rent = models.DecimalField(max_digits=15, decimal_places=2)
    offer = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        verbose_name="What would they like to pay?"
    )
    length_of_lease = models.PositiveSmallIntegerField(help_text='In months')
    move_in_date = models.DateField()
    op = models.PositiveSmallIntegerField(verbose_name='OP%')
    total_broker_fee = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True
    )
