import re

from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property

from penny.constants import DEFAUL_RENT_IMAGE
from penny.model_utils import BaseModel
from penny.utils import image_path, validate_file_size


class RentProperty(BaseModel):
    publisher = models.ForeignKey(get_user_model(),
                                  related_name="rent_properties",
                                  on_delete=models.CASCADE)

    is_listed = models.BooleanField(default=True)

    price = models.PositiveIntegerField()
    contact = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    geopoint = models.CharField(max_length=64)

    about = models.TextField(max_length=1024, blank=True, null=True)

    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    pets_allowed = models.BooleanField(default=True)

    amenities = models.CharField(max_length=255,
                                 help_text="Press Enter to add another amenity")

    @cached_property
    def coords(self):
        lon, lat = re.search('\((.+?)\)', self.geopoint).group(1).split()
        return lat, lon

    @cached_property
    def latitude(self):
        return self.coords[0]

    @cached_property
    def longitude(self):
        return self.coords[1]

    @cached_property
    def default_image(self):
        if self.images.exists():
            return self.images.first().image.url
        return f'{settings.STATIC_URL}{DEFAUL_RENT_IMAGE}'

    @cached_property
    def amenities_list(self):
        return self.amenities.split(",")

    @cached_property
    def detail_link(self):
        return reverse('listing_detail', args=[str(self.id)])

    @cached_property
    def edit_link(self):
        return reverse(
            'admin:rentals_rentproperty_change', args=[str(self.id)])

    def __json__(self, *attrs):
        return {
            **self.attrs(
                'default_image',
                'price',
                'contact',
                'address',
                'latitude',
                'longitude',
                'about',
                'bedrooms',
                'baths',
                'pets_allowed',
                'amenities',
                'detail_link',
                'edit_link',
            ),
            'str': str(self),
            **(self.attrs(*attrs) if attrs else {}),
        }


class RentPropertyImage(BaseModel):
    rent_property = models.ForeignKey(RentProperty,
                                      related_name="images",
                                      on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_path,
                              validators=[validate_file_size])
