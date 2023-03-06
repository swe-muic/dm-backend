"""
This module defines a serializer class for the User model.

The UserSerializer class extends the ModelSerializer class provided by the Django REST framework to automatically
generate serializers for the User model's fields.

The module exports a single class:

- UserSerializer: A serializer class for the User model.

This module is intended to be used as part of a Django REST API for user management.
"""

from rest_framework import serializers

from ..models.user import User


class UserSerializer(serializers.ModelSerializer):
    """A class used to represent a serializer for the User model in Django."""

    class Meta:
        """A class used to set metadata options for the UserSerializer class."""

        model = User
        fields = ("id", "username", "password")
        read_only_fields = ["is_active", "created", "updated"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data: dict) -> User:
        """
        Create and return a new User instance using the validated data.

        Args:
            validated_data (dict):  The validated data for the User instance.

        Returns:
            User: A new User instance created using the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        """
        Update and return an existing User instance, given the validated data.

        Args:
            instance (User): The User instance to update.
            validated_data (dict): The validated data to update the User instance with.

        Returns:
            User: The updated User instance.
        """
        instance.username = validated_data.get("username", instance.username)
        instance.password = validated_data.get("password", instance.password)
        instance.save()
        return instance
