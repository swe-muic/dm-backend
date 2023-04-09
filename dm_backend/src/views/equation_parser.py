"""
EquationParserAPI is a view that simplifies a LaTeX equation and returns the result as a JSON response with http status.

The view accepts GET requests with equation data in the query parameters.
- With GET request, the equation data is parsed using the simplify_latex_expression method of the Expression class,
  from latexvm, and if successful, a new data object is returned in the response.
"""

from latexvm.expression import Expression
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from sympy.parsing.latex import LaTeXParsingError

from ..services.api_renderer import APIRenderer


class EquationParserAPIViewSet(ViewSet):
    """A class used to represent a view for equation parser."""

    renderer_classes = [APIRenderer]

    @action(detail=False, methods=["post"])
    def parse_equation(self, request: Request) -> Response:
        """
        Parse and simplify the LaTeX expression of an equation.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing the original and parsed LaTeX expression,
                or an error response if there was a problem with the input or server.
        """
        try:
            equation = request.data["equation"]
            data = {
                "equation": equation,
                "parsed_equation": Expression.simplify_latex_expression(equation),
            }
            return Response(data, status=status.HTTP_200_OK)
        except LaTeXParsingError as e:
            return Response(
                {"detail": f"LaTeX parsing error - {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"detail": f"Internal server error - {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
