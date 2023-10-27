from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from apps.core.db.models import TimeStampMixin


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_field):
        """Create and save a User with the given email and password"""

        if not email:
            raise ValueError(_("The given email must be set"))
        user = self.model(email=email, **extra_field)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_field):
        """Create and save a regular User with the given username and password"""

        extra_field.setdefault("is_staff", False)
        extra_field.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_field)

    def create_superuser(self, email, password=None, **extra_field):
        """Create and save a SuperUser with the given email and password"""

        extra_field.setdefault("is_superuser", True)
        extra_field.setdefault("is_staff", True)

        if extra_field.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        elif extra_field.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extra_field)


class User(AbstractUser, TimeStampMixin):
    username = models.CharField(max_length=40, verbose_name=_("username"))
    email = models.CharField(max_length=40, unique=True, blank=True, null=True, verbose_name=_("email"))

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email
