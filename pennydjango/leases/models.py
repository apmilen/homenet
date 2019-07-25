import os

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.urls import reverse

from penny.constants import DEFAUL_AVATAR
from penny.models import BaseModel, User
from listings.models import Listing
from leases.constants import (
    LEASE_STATUS, DEFAULT_LEASE_STATUS, APPLICANT_TYPE,
    LEASE_STATUS_PROGRESS
)
from penny.utils import rental_doc_path, validate_file_size


class LeaseCostsManager(models.Manager):
    def total_by_offer(self, lease_id):
        total_obj = self.filter(offer_id=lease_id)\
                        .only('value')\
                        .aggregate(total=models.Sum('value'))
        return total_obj['total'] or 0


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

    def progress_status(self):
        return LEASE_STATUS_PROGRESS.get(self.status, 0)


class LeaseMember(BaseModel):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    offer = models.ForeignKey(Lease, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=155)
    email = models.CharField(max_length=255)
    applicant_type = models.CharField(max_length=155, choices=APPLICANT_TYPE)
    app_fee = models.DecimalField(max_digits=15, decimal_places=2, default=100)
    legal_name = models.CharField(max_length=255, null=True)
    signed_agreement = models.DateField(null=True)
    ip_address = models.CharField(max_length=50, null=True)
    user_agent = models.CharField(max_length=255, null=True)

    @staticmethod
    def avatar():
        return f"{settings.STATIC_URL}{DEFAUL_AVATAR}"

    def get_full_name(self):
        if self.user:
            return self.user.get_full_name()
        return self.name

    def client_detail_link(self):
        return reverse('leases:detail-client', args=[self.id])

    @property
    def total_paid(self):
        paid_amnts = self.transaction_set.aggregate(total_amount=Sum('amount'))
        return paid_amnts.get('total_amount') or 0


class MoveInCost(BaseModel):
    offer = models.ForeignKey(Lease, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    charge = models.CharField(max_length=255)

    objects = LeaseCostsManager()


class RentalApplication(BaseModel):
    lease_member = models.OneToOneField(LeaseMember, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    editing = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True)
    date_of_birth = models.DateField(null=True)
    ssn = models.CharField(max_length=30)
    driver_license = models.CharField(max_length=100, null=True)
    n_of_pets = models.PositiveSmallIntegerField(null=True)
    current_address = models.CharField(max_length=255, null=True)
    current_monthly_rent = models.PositiveIntegerField(null=True)
    landlord_name = models.CharField(max_length=100, null=True)
    landlord_contact = models.CharField(max_length=100, null=True)
    current_company = models.CharField(max_length=100, null=True)
    job_title = models.CharField(max_length=100, null=True)
    annual_income = models.CharField(max_length=100, null=True)
    time_at_current_job = models.CharField(max_length=100, null=True)


class RentalAppDocument(BaseModel):
    rental_app = models.ForeignKey(RentalApplication, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to=rental_doc_path,
        validators=[validate_file_size]
    )

    def filename(self):
        return os.path.basename(self.file.name)
