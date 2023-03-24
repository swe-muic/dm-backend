from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from dm_backend.src.models.equation import Equation
from dm_backend.tests.baker_recipes.equation_baker_recipe import equation_recipe
from dm_backend.tests.baker_recipes.graph_baker_recipe import graph_recipe


class EquationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.get_url = "/api/equations/"
        self.create_url = "/api/equations/"
        self.update_url = lambda equation_id: f"/api/equations/{equation_id}/"
        self.delete_url = lambda equation_id: f"/api/equations/{equation_id}/"
        self.graph = graph_recipe.make(name="test_graph")
        self.valid_payload = {
            "equation": "2x + 3 = 0",
            "parsed_equation": "2x+3=0",
            "color": 1,
            "line_style": "-",
            "line_width": 1,
            "graph": self.graph.id,
        }

    def test_get_equations_empty(self):
        response = self.client.get(self.get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_equations(self):
        equation = equation_recipe.make(**(self.valid_payload | {"graph": self.graph}))
        response = self.client.get(self.get_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], equation.id)

    def test_get_equations_internal_server_error(self):
        with patch("dm_backend.src.views.equation.Equation.objects.all") as mock_query:
            mock_query.side_effect = Exception("Something went wrong")
            response = self.client.get(self.get_url)
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertEqual(
                response.data,
                {"detail": "Internal server error - Something went wrong"},
            )

    def test_create_equation(self):
        response = self.client.post(self.create_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Equation.objects.count(), 1)
        equation = Equation.objects.first()
        self.assertEqual(equation.equation, self.valid_payload["equation"])

    def test_create_invalid_equation(self):
        data = self.valid_payload | {"equation": ""}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_equation(self):
        equation = equation_recipe.make(**(self.valid_payload | {"graph": self.graph}))
        data = self.valid_payload | {"equation": "3x - 5 = 0"}
        response = self.client.put(self.update_url(equation.id), data)
        equation = Equation.objects.filter(id=equation.id).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(equation.equation, data["equation"])

    def test_update_nonexistent_equation(self):
        data = self.valid_payload | {"equation": "3x - 5 = 0"}
        response = self.client.put(self.update_url(999), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_equation(self):
        equation = equation_recipe.make(**(self.valid_payload | {"graph": self.graph}))
        data = self.valid_payload | {"equation": ""}
        response = self.client.put(self.update_url(equation.id), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_equation(self):
        equation = equation_recipe.make(**(self.valid_payload | {"graph": self.graph}))
        response = self.client.delete(self.delete_url(equation.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Equation.objects.filter(id=equation.id).exists())

    def test_delete_nonexistent_equation(self):
        response = self.client.delete(self.delete_url(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue("does not exist" in response.json()["detail"])
