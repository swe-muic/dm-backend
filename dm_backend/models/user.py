"""
This module defines a custom User model for authentication in Django.

The User model extends Django's built-in AbstractBaseUser and PermissionsMixin models and uses a username field for
authentication. It also includes fields for password, staff and active status, and date joined. It uses the
UnicodeUsernameValidator for validating the username field and Django's validate_password function for validating the
password field.

The module exports a single class:

- User: The custom User model class.

This module is intended to be used as part of a Django project for custom user authentication.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    """
    A class used to represent a custom User model for authentication in Django.

    Attributes:
        id (AutoField): The primary key field for the User model.
        username (CharField): The unique username field for authentication.
        password (CharField): The password field for the User model.
        is_staff (BooleanField): A boolean field that designates whether the user is a member of staff.
        is_active (BooleanField): A boolean field that designates whether the user is active.
        date_joined (DateTimeField): The date the user joined the application.

    The class also defines the following fields:
        USERNAME_FIELD (str): The field to use as the unique identifier for authentication.
        REQUIRED_FIELDS (list): A list of fields required for creating a user.
    """

    class Meta:
        """A class used to set metadata options for the User model."""

        verbose_name = "User"
        verbose_name_plural = "Users"

    id = models.AutoField(primary_key=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        validators=[UnicodeUsernameValidator()],
    )
    password = models.CharField(max_length=128, validators=[validate_password])

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # define the field to use as the username field for authentication
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password"]

    def __str__(self) -> str:
        """
        Return a string as a representation of the user.

        Returns:
            str: A string representation of the user
        """
        return f"{self.id}: {self.username}"
