from django.db import models

from penny.models import BaseModel, User
from listings.models import Listing


class Collection(BaseModel):
    name = models.CharField(max_length=64)
    client_email = models.CharField(max_length=64, blank=True)
    client_phone = models.CharField(max_length=64, blank=True)
    notes = models.CharField(max_length=64, blank=True)
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='collections',
    )
    listings = models.ManyToManyField(
        Listing,
        null=True,
        related_name='collections',
    )
