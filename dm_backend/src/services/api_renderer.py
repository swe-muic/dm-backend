"""
This module contains a custom renderer class, APIRenderer, that formats the API response in a standard format.

The API response contains additional metadata such as the HTTP status code and a success/failure message based
on the status code. APIRenderer extends the JSONRenderer class from the Django REST Framework and overrides the render
method to format the data. The render method takes the data, media type, and renderer context as arguments, and returns
a JSON representation of the data with additional metadata.
"""

from rest_framework.renderers import JSONRenderer


class APIRenderer(JSONRenderer):
    """A custom renderer that formats the API response in a standard format."""

    def render(
        self, data: dict, accepted_media_type: str = None, renderer_context: dict = None
    ) -> bytes:
        """
        Render the data to JSON format with additional metadata.

        Args:
            data: The data to be rendered to JSON.
            accepted_media_type: The media type that was requested by the client.
            renderer_context: A dictionary of metadata that provides context for rendering.

        Returns:
            A JSON representation of the data with additional metadata such as the HTTP status code
            and a success/failure message based on the status code.
        """
        response = {}
        response["status"] = renderer_context["response"].status_code
        response["message"] = "success" if response["status"] < 400 else "fail"
        response["data"] = data

        return super().render(response, accepted_media_type, renderer_context)
