"""
SignUpView is a view that creates a new user and generates a JWT token for the user.

The view accepts POST requests with user data in the request body. The user data is validated
using the UserSerializer and if valid, a new user object is created and saved to the database.
A JWT token is then generated for the user using the settings in api_settings.

The view returns a response with the JWT token and a 201 CREATED status if the user was created
successfully.
"""

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from ..serializers.user import UserSerializer


class SignUpView(generics.CreateAPIView):
    """A class used to represent a view for sign-up."""

    serializer_class = UserSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        """
        Create a new user account and return a JWT token for authentication.

        Returns:
            Response: A Response object containing a JWT token for the newly created user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create a JWT token for the user
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({"token": token}, status=status.HTTP_201_CREATED)
