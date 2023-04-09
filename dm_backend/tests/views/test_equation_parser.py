from django.test import TestCase
from latexvm.expression import Expression
from rest_framework import status
from rest_framework.test import APIClient


class EquationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/viewset/equations/parser/parse_equation/"

    def test_get_parsed_equation(self):
        test_cases = [
            "x + x",
            "y = x / 2",
            "2 \\times x + 3 = 0",
        ]
        for i, test_case in enumerate(test_cases):
            expected_output = Expression.simplify_latex_expression(test_case)
            with self.subTest(
                test_number=i, input=test_case, expected_output=expected_output
            ):
                payload = {"equation": test_case}
                response = self.client.post(self.url, payload)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.json()["message"], "success")
                self.assertEqual(response.data["parsed_equation"], expected_output)

    def test_get_latex_parsing_error(self):
        test_cases = [
            "$x + x",
            "y = \frac{x}{2}",
            "2$x$ + 3 = 0",
        ]
        for i, test_case in enumerate(test_cases):
            print(test_case)
            with self.subTest(test_number=i, input=test_case):
                payload = {"equation": test_case}
                response = self.client.post(self.url, payload)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.json()["message"], "fail")
                self.assertTrue("LaTeX parsing error" in response.data["detail"])

    def test_get_equations_internal_server_error(self):
        response = self.client.post(self.url, None)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json()["message"], "fail")
        self.assertTrue("Internal server error" in response.data["detail"])
