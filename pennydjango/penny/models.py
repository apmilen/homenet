from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractUser, UserManager

from penny.model_utils import BaseModel
from penny.utils import avatar_path, validate_file_size
from penny.constants import DEFAUL_AVATAR


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

    @cached_property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return f"{settings.STATIC_URL}{DEFAUL_AVATAR}"
