import re

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import cached_property

from penny.models import User
from penny.model_utils import BaseModel
from penny.utils import image_path, validate_file_size


class RentProperty(BaseModel):
    publisher = models.ForeignKey(get_user_model(),
                                  related_name="rent_properties",
                                  on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    contact = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    geopoint = models.CharField(max_length=64)
    # pictures = NOIDEA
    about = models.TextField(max_length=512, blank=True, null=True)

    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    pets_allowed = models.BooleanField(default=True)

    amenities = models.TextField()

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


class RentPropertyImage(BaseModel):
    rent_property = models.ForeignKey(RentProperty,
                                      related_name="images",
                                      on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_path,
                              validators=[validate_file_size])


class Availability(BaseModel):
    agent = models.OneToOneField(User, on_delete=models.CASCADE)
    reference_property = models.OneToOneField(RentProperty,
                                              on_delete=models.CASCADE)

    radius = models.PositiveIntegerField(default=1000)

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
