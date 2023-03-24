"""
This module defines a serializer class for the Equation model.

The EquationSerializer class extends the ModelSerializer class provided by the Django REST framework to automatically
generate serializers for the Equation model's fields.

The module exports a single class:

- EquationSerializer: A serializer class for the Equation model.

This module is intended to be used as part of a Django REST API.
"""

from rest_framework import serializers

from ..models.equation import Equation


class EquationSerializer(serializers.ModelSerializer):
    """A class used to represent a serializer for the Equation model in Django."""

    class Meta:
        """A class used to set metadata options for the EquationSerializer class."""

        model = Equation
        fields = [
            "id",
            "equation",
            "parsed_equation",
            "color",
            "line_style",
            "line_width",
            "graph",
        ]
        read_only_fields = ["id"]
