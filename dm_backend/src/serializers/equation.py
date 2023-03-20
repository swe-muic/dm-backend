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

    def create(self, validated_data: dict) -> Equation:
        """
        Create and return a new Equation instance using the validated data.

        Args:
            validated_data (dict):  The validated data for the Equation instance.

        Returns:
            Equation: A new Equation instance created using the validated data.
        """
        return Equation.objects.create(**validated_data)

    def update(self, instance: Equation, validated_data: dict) -> Equation:
        """
        Update and return an existing Equation instance, given the validated data.

        Args:
            instance (Equation): The Equation instance to update.
            validated_data (dict): The validated data to update the Equation instance with.

        Returns:
            Equation: The updated Equation instance.
        """
        instance.equation = validated_data.get("equation", instance.equation)
        instance.parsed_equation = validated_data.get(
            "parsed_equation", instance.parsed_equation
        )
        instance.color = validated_data.get("color", instance.color)
        instance.line_style = validated_data.get("line_style", instance.line_style)
        instance.line_width = validated_data.get("line_width", instance.line_width)
        instance.save()
        return instance
