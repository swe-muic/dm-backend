"""
GraphAPIViewSet is a view that creates a new graph with the specified data.

The view accepts GET, POST, PUT and DELETE requests with graph data in the request body.
- With GET request, all the graphs in the database are fetched and returned as a list of graph objects.
- With POST request, the graph data is validated using the GraphSerializer, and if valid, a new graph object is
  created and saved to the database.
- With PUT request, the graph with the specified graph_id will be updated according to the new graph data.
- With DELETE request, the graph with the specified graph_id will be deleted from the database.
"""

from rest_framework.viewsets import ModelViewSet

from ..models.graph import Graph
from ..serializers.graph import GraphSerializer
from ..services.api_renderer import APIRenderer


class GraphAPIViewSet(ModelViewSet):
    """A class used to represent a view for graph."""

    queryset = Graph.objects.all()
    serializer_class = GraphSerializer
    renderer_classes = [APIRenderer]
