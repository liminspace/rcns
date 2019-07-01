from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserQuerySet(models.QuerySet):
    pass


class CustomUserManager(UserManager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)


class User(AbstractUser):
    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'userauth_user'

    def login(self, request):
        self.backend = settings.AUTHENTICATION_BACKENDS[settings.MODEL_AUTHENTICATION_BACKEND_IX]
        auth_login(request, self)
