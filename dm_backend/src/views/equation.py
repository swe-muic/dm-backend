"""
EquationAPIViewSet is a view that creates a new equation with the specified data.

The view accepts GET, POST, PUT and DELETE requests with equation data in the request body.
- With GET request, all the equations in the database are fetched and returned as a list of equation objects.
- With POST request, the equation data is validated using the EquationSerializer, and if valid, a new equation object is
  created and saved to the database.
- With PUT request, the equation with the specified equation_id will be updated according to the new equation data.
- With DELETE request, the equation with the specified equation_id will be deleted from the database.
"""

from rest_framework.viewsets import ModelViewSet

from ..models.equation import Equation
from ..serializers.equation import EquationSerializer
from ..services.api_renderer import APIRenderer


class EquationAPIViewSet(ModelViewSet):
    """A class used to represent a view for equation."""

    queryset = Equation.objects.all()
    serializer_class = EquationSerializer
    renderer_classes = [APIRenderer]
