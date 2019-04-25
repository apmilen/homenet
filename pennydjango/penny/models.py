from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractUser, UserManager

from .model_utils import BaseModel


class CaseInsensitiveUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)


class User(AbstractUser, BaseModel):
    objects = CaseInsensitiveUserManager()

    # id = models.UUIDField
    # username
    # password
    # email
    # first_name
    # last_name
    # is_active
    # is_staff
    # is_superuser
    # last_login
    # date_joined


class Availability(BaseModel):
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    reference_property = models.ForeignKey('rentals.RentProperty',
                                           on_delete=models.CASCADE)

    radius = models.PositiveIntegerField(default=1000)

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    @cached_property
    def available_time(self):
        return self.end_datetime - self.start_datetime

    @cached_property
    def is_active(self):
        return self.start_datetime <= timezone.now() <= self.end_datetime
