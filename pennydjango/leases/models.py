from django.conf import settings
from django.db import models
from django.urls import reverse

from penny.constants import DEFAUL_AVATAR
from penny.models import BaseModel, User
from listings.models import Listing
from leases.constants import LEASE_STATUS, DEFAULT_LEASE_STATUS, APPLICANT_TYPE


class LeaseCostsManager(models.Manager):
    def total_by_offer(self, lease_id):
        total_obj = self.filter(offer_id=lease_id)\
                        .only('value')\
                        .aggregate(total=models.Sum('value'))
        return total_obj['total']


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
    op_received_at = models.DateField(null=True)
    status = models.CharField(
        max_length=50,
        choices=LEASE_STATUS,
        default=DEFAULT_LEASE_STATUS
    )

    def detail_link(self):
        return reverse('leases:detail', args=[self.id])


class LeaseMember(BaseModel):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    offer = models.ForeignKey(Lease, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=155)
    email = models.CharField(max_length=255)
    applicant_type = models.CharField(max_length=155, choices=APPLICANT_TYPE)
    app_fee = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    legal_name = models.CharField(max_length=255, null=True)
    signed_agreement = models.DateField(null=True)

    @staticmethod
    def avatar():
        return f"{settings.STATIC_URL}{DEFAUL_AVATAR}"

    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()
        return self.name


class MoveInCost(BaseModel):
    offer = models.ForeignKey(Lease, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    charge = models.CharField(max_length=255)

    objects = LeaseCostsManager()
