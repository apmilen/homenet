from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractUser, UserManager

from penny.model_utils import BaseModel
from penny.constants import NEIGHBORHOODS, DAYS


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

    neighborhood = models.CharField(
        choices=NEIGHBORHOODS,
        max_length=128
    )

    start_day = models.CharField(
        choices=((d, d) for d in DAYS),
        max_length=16
    )
    end_day = models.CharField(
        choices=((d, d) for d in DAYS),
        max_length=16
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    @cached_property
    def available_time(self):
        return self.end_time.hour - self.start_time.hour

    @cached_property
    def is_active(self):
        dt_now = timezone.now()
        start_day = DAYS.index(self.start_day)
        end_day = DAYS.index(self.end_day)
        conditions = (
            self.start_time <= dt_now.time() <= self.end_time,
            start_day <= dt_now.weekday() <= end_day
        )
        return all(conditions)
