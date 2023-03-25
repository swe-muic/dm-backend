"""
GraphAPI is a view that creates a new graph with the specified data.

The view accepts GET, POST, PUT and DELETE requests with graph data in the request body.
- With GET request, all the graphs in the database are fetched and returned as a list of graph objects.
- With POST request, the graph data is validated using the GraphSerializer, and if valid, a new graph object is
  created and saved to the database.
- With PUT request, the graph with the specified graph_id will be updated according to the new graph data.
- With DELETE request, the graph with the specified graph_id will be deleted from the database.
"""

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.graph import Graph
from ..serializers.graph import GraphSerializer


class GraphAPI(APIView):
    """A class used to represent a view for graph."""

    def get_all(self, request: Request) -> Response:
        """
        Fetch all graphs and return a JSON response with http status.

        Args:
            request (Request): A request containing the graph data.

        Returns:
            Response: A Response object containing a list of graphs or details for error.
        """
        try:
            graphs = Graph.objects.all()
            serializer = GraphSerializer(graphs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": f"Internal server error - {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request: Request, graph_id: int = None) -> Response:
        """
        Fetch a single graph if the graph_id is specified; otherwise, fetch all graphs, and return a JSON response with http status.

        Args:
            request (Request): A request containing the graph data.
            graph_id (int): The id of an existing graph.

        Returns:
            Response: A Response object containing a single graph or details for error.
        """
        if graph_id is None:
            return self.get_all(request)
        try:
            graph = Graph.objects.get(id=graph_id)
            serializer = GraphSerializer(graph)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Graph.DoesNotExist:
            return Response(
                {"detail": f"Graph with id {graph_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"detail": f"Internal server error - {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request: Request) -> Response:
        """
        Create a new graph and return JSON response with http status.

        Args:
            request (Request): A request containing the graph data.

        Returns:
            Response: A Response object containing the created graph or details for error.
        """
        try:
            serializer = GraphSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            graph = serializer.save()
            return Response(GraphSerializer(graph).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": f"Internal server error - {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request: Request, graph_id: int) -> Response:
        """
        Update an existing graph with the specified graph_id and return JSON response with http status.

        Args:
            request (Request): A request containing the graph data.
            graph_id (int): The id of an existing graph.

        Returns:
            Response: A Response object containing the updated graph or details for error.
        """
        try:
            graph = Graph.objects.get(id=graph_id)
            serializer = GraphSerializer(graph, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Graph.DoesNotExist:
            return Response(
                {"detail": f"Graph with id {graph_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": f"Internal server error - {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request: Request, graph_id: int) -> Response:
        """
        Delete an existing graph with the specified graph_id and return JSON response with http status.

        Args:
            request (Request): A request containing the graph data.
            graph_id (int): The id of an existing graph.

        Returns:
            Response: A Response object containing the deleted graph or details for error.
        """
        try:
            graph = Graph.objects.get(id=graph_id)
            graph.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Graph.DoesNotExist:
            return Response(
                {"detail": f"Graph with id {graph_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"detail": f"Internal server error - {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
