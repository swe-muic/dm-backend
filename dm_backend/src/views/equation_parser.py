"""
EquationParserAPI is a view that simplifies a LaTeX equation and returns the result as a JSON response with http status.

The view accepts GET requests with equation data in the query parameters.
- With POST request, the equation data is parsed using the simplify_latex_expression method of the Expression class,
  from latexvm, and if successful, a new data object is returned in the response.
"""

from latexvm.graph_session import GraphSession
from latexvm.type_defs import ResultType
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
    def parse_expressions(self, request: Request) -> Response:
        """
        Resolve and parse a given list of a mathematical expressions containing a function call.

        The function call will be resolved by substituting it with its value based on the function defined in the
        environment. The resulting expression will then be parsed as a LaTeX string.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: A JSON response containing the original and parsed expressions,
                or an error response if there was a problem with the input or server.
        """
        try:
            expressions = request.data["expressions"]
            graph_session = GraphSession.new()
            graph_session.add_sub_rule(r"\*\*", "^")
            parsed_expressions = []
            for expression in expressions:
                parsed_expression = graph_session.force_resolve_function(expression)
                if parsed_expression.result == ResultType.FAILURE:
                    raise LaTeXParsingError(f"{expression} is invalid")
                parsed_expressions.append(parsed_expression.message)
            data = {
                "expressions": expressions,
                "parsed_expressions": parsed_expressions,
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
