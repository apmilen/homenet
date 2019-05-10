from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractUser, UserManager

from penny.model_utils import BaseModel
from penny.constants import (
    DEFAUL_AVATAR, USER_TYPE, ADMIN_TYPE, AGENT_TYPE, CLIENT_TYPE
)
from penny.utils import avatar_path, validate_file_size


class CaseInsensitiveUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(username__iexact=username)


class UserTypeManager(CaseInsensitiveUserManager):
    def create_agent(self, *args, **kwargs):
        user = self.create_user(*args, **kwargs)
        user.user_type = AGENT_TYPE
        user.save()
        return user

    def create_admin(self, *args, **kwargs):
        user = self.create_user(*args, **kwargs)
        user.user_type = ADMIN_TYPE
        user.save()
        return user

    def create_client(self, *args, **kwargs):
        user = self.create_user(*args, **kwargs)
        user.user_type = CLIENT_TYPE
        user.save()
        return user


class User(AbstractUser, BaseModel):
    objects = UserTypeManager()

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.perms = PermissionManager(self)

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


class PermissionManager:
    def __init__(self, user: User):
        self.user = user

    def has_admin_access(self):
        return any([
            self.user.is_superuser,
            self.user.is_user_admin
        ])

    def has_agent_access(self):
        return any([
            self.has_admin_access(),
            self.user.is_user_agent
        ])

    def has_client_access(self):
        return any([
            self.has_admin_access(),
            self.user.is_user_client
        ])

    def has_client_or_agent_access(self):
        return any([
            self.has_admin_access(),
            self.user.is_user_agent,
            self.user.is_user_client
        ])
