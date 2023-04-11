import json

from django.test import TestCase
from latexvm.graph_session import GraphSession
from rest_framework import status
from rest_framework.test import APIClient


class EquationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/viewset/equations/parser/parse_expressions/"

    def test_get_parsed_expressions(self):
        test_cases = [
            ["y(x) = x / 2"],
            ["x = 2", "x ^ x"],
            ["h(x) = x*2", "f(x) = x*(h(x))", "f(3)", "what = f(3)*2", "what"],
        ]
        for i, test_case in enumerate(test_cases):
            graph_session = GraphSession.new()
            expected_output = []
            for expression in test_case:
                simplified_expression = graph_session.execute(expression).message
                parsed_expression = graph_session.force_resolve_function(
                    simplified_expression
                ).message
                expected_output.append(parsed_expression)
            with self.subTest(
                test_number=i, input=test_case, expected_output=expected_output
            ):
                payload = {"expressions": test_case}
                response = self.client.post(
                    self.url, json.dumps(payload), content_type="application/json"
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.json()["message"], "success")
                self.assertEqual(response.data["parsed_expressions"], expected_output)

    def test_get_latex_parsing_error(self):
        test_cases = [
            ["y = \frac{x}{2}"],
            ["x = 2", "$x ^ x"],
            ["2$x$ + 3 = 0"],
        ]
        for i, test_case in enumerate(test_cases):
            with self.subTest(test_number=i, input=test_case):
                payload = {"expressions": test_case}
                response = self.client.post(
                    self.url, json.dumps(payload), content_type="application/json"
                )
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertEqual(response.json()["message"], "fail")
                self.assertTrue("LaTeX parsing error" in response.data["detail"])

    def test_get_equations_internal_server_error(self):
        response = self.client.post(self.url, None)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.json()["message"], "fail")
        self.assertTrue("Internal server error" in response.data["detail"])
