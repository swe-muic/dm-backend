from django.test import TestCase

from dm_backend.tests.baker_recipes.equation_baker_recipe import equation_recipe
from dm_backend.tests.baker_recipes.graph_baker_recipe import graph_recipe


class TestEquation(TestCase):
    def test_create_equation(self):
        equation_str = "y = 2x + 1"
        equation = equation_recipe.make(equation=equation_str)
        self.assertEqual(equation.equation, equation_str)

    def test_create_equation_with_graph(self):
        graph_name = "graph1"
        graph = graph_recipe.make(name=graph_name)
        equation = equation_recipe.make(graph=graph)
        self.assertEqual(equation.graph.name, graph_name)
