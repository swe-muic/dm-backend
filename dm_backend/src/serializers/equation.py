from rest_framework import serializers

from ..models.equation import Equation


class EquationSerializer(serializers.ModelSerializer):

    class Meta:

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
        print('this is create')
        return Equation.objects.create(**validated_data)

    def update(self, instance: Equation, validated_data: dict) -> Equation:
        print('this is update')
        instance.equation = validated_data.get("equation", instance.equation)
        instance.parsed_equation = validated_data.get("parsed_equation", instance.parsed_equation)
        instance.color = validated_data.get("color", instance.color)
        instance.line_style = validated_data.get("line_style", instance.line_style)
        instance.line_width = validated_data.get("line_width", instance.line_width)
        instance.save()
        return instance
