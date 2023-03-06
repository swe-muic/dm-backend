from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password


class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    id = models.AutoField(primary_key=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[UnicodeUsernameValidator()]
    )
    password = models.CharField(
        max_length=128,
        validators=[validate_password]
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # define the field to use as the username field for authentication
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return f"{self.id}: {self.username}"
