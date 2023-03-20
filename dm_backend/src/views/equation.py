from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from ..models.equation import Equation
from ..serializers.equation import EquationSerializer


class EquationAPI(APIView):

    def post(self, request: Request) -> Response:
        serializer = EquationSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            equation_id = request.data.get("id", None)
            equation = Equation.objects.get(id=equation_id) if equation_id else None
            if equation:
                equation = serializer.update(equation, request.data)
                http_status = status.HTTP_200_OK
            else:
                equation = serializer.save()
                http_status = status.HTTP_201_CREATED
            return Response(EquationSerializer(equation).data, status=http_status)
        except ValidationError:
            return Response(
                {"detail": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Internal server error - {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
