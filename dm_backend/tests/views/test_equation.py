from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from dm_backend.src.models.equation import Equation
from dm_backend.tests.baker_recipes.equation_baker_recipe import equation_recipe
from dm_backend.tests.baker_recipes.graph_baker_recipe import graph_recipe


class EquationAPIViewSetTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/viewset/equations/"
        self.url_id = lambda equation_id: f"{self.url}{equation_id}/"
        self.graph = graph_recipe.make(name="test_graph")
        self.valid_payload = {
            "equation": "2x+3=0",
            "parsed_equation": "2x + 3 = 0",
            "color": 1,
            "line_style": "polyline",
            "line_width": 1,
            "graph": self.graph.id,
        }

    def test_get_all_equations_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(len(response.data), 0)

    def test_get_all_equations(self):
        equation = equation_recipe.make(**(self.valid_payload | {"graph": self.graph}))
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], equation.id)

    def test_get_equation(self):
        equation = equation_recipe.make(**(self.valid_payload | {"graph": self.graph}))
        response = self.client.get(self.url_id(equation.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(response.data["equation"], equation.equation)

    def test_get_nonexistent_equation(self):
        response = self.client.get(self.url_id(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "fail")
        self.assertEqual(response.data["detail"], "Not found.")

    def test_create_equation(self):
        response = self.client.post(self.url, self.valid_payload)
        equation = Equation.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(Equation.objects.count(), 1)
        self.assertEqual(equation.equation, self.valid_payload["equation"])

    def test_create_invalid_equation(self):
        payload = self.valid_payload | {"equation": ""}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "fail")
        self.assertEqual(Equation.objects.count(), 0)

    def test_update_equation(self):
        equation = equation_recipe.make(**(self.valid_payload | {"graph": self.graph}))
        payload = self.valid_payload | {"equation": "3x - 5 = 0"}
        response = self.client.put(self.url_id(equation.id), payload)
        equation = Equation.objects.filter(id=equation.id).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(equation.equation, payload["equation"])

    def test_update_nonexistent_equation(self):
        payload = self.valid_payload | {"equation": "3x - 5 = 0"}
        response = self.client.put(self.url_id(999), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "fail")
        self.assertEqual(response.data["detail"], "Not found.")

    def test_update_invalid_equation(self):
        equation = equation_recipe.make(**(self.valid_payload | {"graph": self.graph}))
        payload = self.valid_payload | {"equation": ""}
        response = self.client.put(self.url_id(equation.id), payload)
        equation = Equation.objects.filter(id=equation.id).first()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "fail")
        self.assertEqual(equation.equation, self.valid_payload["equation"])

    def test_delete_equation(self):
        equation = equation_recipe.make(**(self.valid_payload | {"graph": self.graph}))
        response = self.client.delete(self.url_id(equation.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Equation.objects.filter(id=equation.id).exists())
        self.assertEqual(Equation.objects.count(), 0)

    def test_delete_nonexistent_equation(self):
        response = self.client.delete(self.url_id(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "fail")
        self.assertEqual(response.data["detail"], "Not found.")
