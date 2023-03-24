"""
This module defines a serializer class for the Graph model.

The GraphSerializer class extends the ModelSerializer class provided by the Django REST framework to automatically
generate serializers for the Graph model's fields.

The module exports a single class:

GraphSerializer: A serializer class for the Graph model.
This module is intended to be used as part of a Django REST API.
"""

from rest_framework import serializers

from ..models.graph import Graph


class GraphSerializer(serializers.ModelSerializer):
    """A class used to represent a serializer for the Graph model in Django."""

    class Meta:
        """A class used to set metadata options for the GraphSerializer class."""

        model = Graph
        fields = [
            "id",
            "name",
            "preview",
            "owner",
            "created",
            "updated",
        ]
        read_only_fields = ["id", "created", "updated"]
