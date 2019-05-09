from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractUser, UserManager

from penny.model_utils import BaseModel
from penny.constants import DEFAUL_AVATAR, NEIGHBORHOODS, DAYS, USER_TYPE
from penny.utils import avatar_path, validate_file_size


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

    avatar = models.ImageField(
        upload_to=avatar_path,
        validators=[validate_file_size],
        blank=True, null=True
    )

    user_type = models.CharField(max_length=255, choices=USER_TYPE)

    @cached_property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return f"{settings.STATIC_URL}{DEFAUL_AVATAR}"

    def __getattr__(self, name):
        """
        Used to compute an attribute starting with 'is_user_' followed by a
        user type, returning True if the user is that type, False otherwise
        :param name: attribute name starting with 'is_user_'
        :return: Boolean True if is the specified user type
        """
        if name.startswith('is_user_'):
            usertype = name[8:]
            return usertype == str(self.user_type)
        raise AttributeError(f"{self} object has not attribute '{name}'")


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
