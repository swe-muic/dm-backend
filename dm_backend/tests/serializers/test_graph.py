from django.test import TestCase

from dm_backend.src.models.graph import Graph
from dm_backend.src.serializers.graph import GraphSerializer


class GraphSerializerTest(TestCase):
    def setUp(self):
        self.create_url = "/api/graphs/"
        self.update_url = lambda graph_id: f"/api/graphs/{graph_id}/"
        self.validated_data = {
            "name": "test_graph",
            "owner": "test_owner",
        }

    def test_create_graph(self):
        serializer = GraphSerializer()
        graph = serializer.create(self.validated_data)
        self.assertIsInstance(graph, Graph)
        self.assertEqual(graph.name, self.validated_data["name"])
        self.assertEqual(graph.owner, self.validated_data["owner"])

    def test_update_graph(self):
        graph = Graph.objects.create(**self.validated_data)
        serializer = GraphSerializer()
        updated_graph = serializer.update(
            graph, self.validated_data | {"name": "updated_graph"}
        )
        self.assertEqual(updated_graph.name, "updated_graph")
