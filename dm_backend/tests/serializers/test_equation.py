from django.test import TestCase

from dm_backend.src.models.equation import Equation
from dm_backend.src.serializers.equation import EquationSerializer
from dm_backend.tests.baker_recipes.graph_baker_recipe import graph_recipe


class EquationSerializerTest(TestCase):
    def setUp(self):
        self.create_url = "/api/equations/"
        self.update_url = lambda equation_id: f"/api/equations/{equation_id}/"
        self.graph = graph_recipe.make(name="test_graph")
        self.validated_data = {
            "equation": "2x + 3 = 0",
            "parsed_equation": "2x+3=0",
            "color": 1,
            "line_style": "-",
            "line_width": 1,
            "graph": self.graph,
        }

    def test_create_equation(self):
        serializer = EquationSerializer()
        equation = serializer.create(self.validated_data)
        self.assertIsInstance(equation, Equation)
        self.assertEqual(equation.equation, self.validated_data["equation"])
        self.assertEqual(
            equation.parsed_equation, self.validated_data["parsed_equation"]
        )
        self.assertEqual(equation.color, self.validated_data["color"])
        self.assertEqual(equation.line_style, self.validated_data["line_style"])
        self.assertEqual(equation.line_width, self.validated_data["line_width"])

    def test_update_equation(self):
        equation = Equation.objects.create(**self.validated_data)
        serializer = EquationSerializer()
        updated_equation = serializer.update(
            equation, self.validated_data | {"equation": "y = 2x"}
        )
        self.assertEqual(updated_equation.equation, "y = 2x")
