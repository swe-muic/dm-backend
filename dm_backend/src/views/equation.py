"""
EquationAPI is a view that creates a new equation with the specified data.

The view accepts POST and PUT requests with equation data in the request body.
- With POST request, the equation data is validated using the EquationSerializer, and if valid, a new equation object is
  created and saved to the database.
- With PUT request, the equation with the specified equation_id will be updated according to the new equation data.
"""

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.equation import Equation
from ..serializers.equation import EquationSerializer


class EquationAPI(APIView):
    """A class used to represent a view for equation."""

    def post(self, request: Request) -> Response:
        """
        Create a new equation and return JSON response with http status.

        Args:
            request (Request): A request containing the equation data.

        Returns:
            Response: A Response object containing the created equation or details for error.
        """
        try:
            serializer = EquationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            equation = serializer.save()
            return Response(
                EquationSerializer(equation).data, status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": f"Internal server error - {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request: Request, equation_id: int) -> Response:
        """
        Update an existing equation with the specified equation_id and return JSON response with http status.

        Args:
            request (Request): A request containing the equation data.
            equation_id (int): The id of an existing equation.

        Returns:
            Response: A Response object containing the updated equation or details for error.
        """
        try:
            equation = Equation.objects.get(id=equation_id)
            serializer = EquationSerializer(equation, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Equation.DoesNotExist:
            return Response(
                {"detail": f"Equation with id {equation_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": f"Internal server error - {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request: Request, equation_id: int) -> Response:
        """
        Delete an existing equation with the specified equation_id and return JSON response with http status.

        Args:
            request (Request): A request containing the equation data.
            equation_id (int): The id of an existing equation.

        Returns:
            Response: A Response object containing the deleted equation or details for error.
        """
        try:
            equation = Equation.objects.get(id=equation_id)
            equation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Equation.DoesNotExist:
            return Response(
                {"detail": f"Equation with id {equation_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"detail": f"Internal server error - {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
