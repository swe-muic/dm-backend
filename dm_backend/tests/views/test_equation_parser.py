from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class EquationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.get_url = "/api/equations/parser/"
        self.valid_payload = {
            "equation": "y = x / 2",
        }
        self.invalid_payload = {
            "equation": "y = \frac{x}{2}",
        }

    def test_get_parsed_equation(self):
        response = self.client.get(self.get_url, data=self.valid_payload)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["parsed_equation"], "x = 2 y")
        self.valid_payload["equation"] = "2 \\times x + 3 = 0"
        response = self.client.get(self.get_url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["parsed_equation"], "x = - \\frac{3}{2}")

    def test_get_latex_parsing_error(self):
        response = self.client.get(self.get_url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("parsing error" in response.json()["detail"])
        self.invalid_payload["equation"] = "$x = 2$"
        response = self.client.get(self.get_url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("parsing error" in response.json()["detail"])

    def test_get_equations_internal_server_error(self):
        response = self.client.get(self.get_url, data=None)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertTrue("Internal server error" in response.json()["detail"])
