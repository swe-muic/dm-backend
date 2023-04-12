from django.test import TestCase

from dm_backend.src.models.equation import Equation
from dm_backend.src.serializers.equation import EquationSerializer
from dm_backend.tests.baker_recipes.graph_baker_recipe import graph_recipe


class EquationSerializerTest(TestCase):
    def setUp(self):
        self.graph = graph_recipe.make(name="test_graph")
        self.validated_data = {
            "equation": "2x+3=0",
            "parsed_equation": "2x + 3 = 0",
            "color": 1,
            "line_style": "polyline",
            "line_width": 1,
            "graph": self.graph,
        }
        self.equation = Equation.objects.create(**self.validated_data)
        self.serializer = EquationSerializer(instance=self.equation)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            [
                "id",
                "equation",
                "parsed_equation",
                "color",
                "line_style",
                "line_width",
                "graph",
            ],
        )

    def test_equation_field_content(self):
        """Test that the equation field has the expected content."""
        data = self.serializer.data
        self.assertEqual(data["equation"], self.validated_data["equation"])

    def test_parsed_equation_field_content(self):
        """Test that the parsed_equation field has the expected content."""
        data = self.serializer.data
        self.assertEqual(
            data["parsed_equation"], self.validated_data["parsed_equation"]
        )

    def test_color_field_content(self):
        """Test that the color field has the expected content."""
        data = self.serializer.data
        self.assertEqual(data["color"], self.validated_data["color"])

    def test_line_style_field_content(self):
        """Test that the line_style field has the expected content."""
        data = self.serializer.data
        self.assertEqual(data["line_style"], self.validated_data["line_style"])

    def test_graph_field_content(self):
        """Test that the graph field has the expected content."""
        data = self.serializer.data
        self.assertEqual(data["graph"], self.validated_data["graph"].id)

    def test_line_width_field_content(self):
        """Test that the line_width field has the expected content."""
        data = self.serializer.data
        self.assertEqual(data["line_width"], self.validated_data["line_width"])

    def test_create_equation(self):
        """Test that the equation instance is created correctly."""
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
        """Test that the equation instance is updated correctly."""
        equation = Equation.objects.create(**self.validated_data)
        serializer = EquationSerializer()
        updated_equation = serializer.update(
            equation, self.validated_data | {"equation": "y = 2x"}
        )
        self.assertEqual(updated_equation.equation, "y = 2x")
