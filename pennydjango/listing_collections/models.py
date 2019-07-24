from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from penny.models import BaseModel, User
from penny.constants import DEFAUL_RENT_IMAGE
from listings.models import Listing


class Collection(BaseModel):
    name = models.CharField(max_length=32)
    notes = models.TextField()
    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='collections',
    )
    listings = models.ManyToManyField(
        Listing,
        related_name='collections',
    )

    def __json__(self, *attrs):
        return {
            **self.attrs(
                'id',
                'name',
                'notes',
            ),
            'str': str(self),
            **(self.attrs(*attrs) if attrs else {}),
        }

    @cached_property
    def default_image(self):
        listing = self.listings.first()
        if listing:
            return listing.default_image

        return f'{settings.STATIC_URL}{DEFAUL_RENT_IMAGE}'
