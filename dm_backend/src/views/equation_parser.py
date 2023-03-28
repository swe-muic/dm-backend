"""
EquationParserAPI is a view that simplifies a LaTeX equation and returns the result as a JSON response with http status.

The view accepts GET requests with equation data in the query parameters.
- With GET request, the equation data is parsed using the simplify_latex_expression method of the Expression class,
  from latexvm, and if successful, a new data object is returned in the response.
"""

from latexvm.expression import Expression
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from sympy.parsing.latex import LaTeXParsingError


class EquationParserAPI(APIView):
    """A class used to represent a view for equation parser."""

    def get(self, request: Request) -> Response:
        """
        Handle HTTP GET requests to simplify a LaTeX expression.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing the original and parsed LaTeX expression,
                or an error response if there was a problem with the input or server.
        """
        data = {}
        try:
            data["equation"] = request.query_params.get("equation")
            data["parsed_equation"] = Expression.simplify_latex_expression(
                data["equation"]
            )
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
