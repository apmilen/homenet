from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.functional import cached_property
from django.contrib.auth.models import AbstractUser, UserManager

from job_applications.models import JobApplication
from penny.model_utils import BaseModel
from penny.constants import (
    DEFAUL_AVATAR, USER_TYPE, ADMIN_TYPE, AGENT_TYPE, CLIENT_TYPE
)
from penny.utils import avatar_path, validate_file_size


class CaseInsensitiveUserManager(UserManager):
    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)


class UserTypeManager(CaseInsensitiveUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("user_type", 'admin')
        return self._create_user(email, password, **extra_fields)

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
    # password
    # email
    # first_name
    # last_name
    # is_active
    # is_staff
    # is_superuser
    # last_login
    # date_joined
    email = models.EmailField('email address', unique=True)
    job_application = models.OneToOneField(
        JobApplication,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    ) 

    avatar = models.ImageField(
        upload_to=avatar_path,
        validators=[validate_file_size],
        blank=True, null=True
    )

    user_type = models.CharField(max_length=255, choices=USER_TYPE)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.perms = PermissionManager(self)

    def __json__(self, *attrs):
        return {
            **self.attrs(
                'id',
                'email',
                'first_name',
                'last_name',
                'date_joined',
                'avatar_url',
                'profile_link',
                'is_active',
                'is_staff',
                'is_superuser',
                'is_authenticated',
                'is_user_admin',
                'is_user_agent',
                'is_user_client',
                'user_type',
                'user_type_str',
                'collections_list'
            ),
            'str': str(self),
            **(self.attrs(*attrs) if attrs else {}),
        }

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

    @cached_property
    def profile_link(self):
        return reverse('userprofile', args=[self.id])

    @cached_property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return f"{settings.STATIC_URL}{DEFAUL_AVATAR}"

    @cached_property
    def user_type_str(self):
        return self.get_user_type_display()

    @cached_property
    def collections_list(self):
        return [collection.__json__() for collection in self.collections.all()]


class PermissionManager:
    def __init__(self, user: User):
        self.user = user

    def has_admin_access(self):
        return self.user.is_superuser or self.user.is_user_admin

    def has_agent_access(self):
        return self.user.is_user_agent or self.has_admin_access()

    def has_client_access(self):
        return self.user.is_user_client or self.has_admin_access()

    def has_client_or_agent_access(self):
        return self.has_client_access() or self.has_agent_access()
