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
