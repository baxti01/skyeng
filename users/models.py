from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import MyUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True, verbose_name='email')

    first_name = models.CharField(max_length=100, blank=True, verbose_name='first name')
    last_name = models.CharField(max_length=100, blank=True, verbose_name='last name')

    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='date joined')
    is_active = models.BooleanField(default=True, verbose_name='is active')
    is_staff = models.BooleanField(default=False, verbose_name='is staff')
    is_superuser = models.BooleanField(default=False, verbose_name='is superuser')

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    def __str__(self):
        return self.email
