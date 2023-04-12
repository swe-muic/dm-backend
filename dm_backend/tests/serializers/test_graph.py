from django.test import TestCase

from dm_backend.src.models.graph import Graph
from dm_backend.src.serializers.graph import GraphSerializer


class GraphSerializerTest(TestCase):
    def setUp(self):
        self.validated_data = {
            "name": "test_graph",
            "owner": "test_owner",
        }
        self.graph = Graph.objects.create(**self.validated_data)
        self.serializer = GraphSerializer(instance=self.graph)

    def test_contains_expected_fields(self):
        """Test that the serializer contains the expected fields."""
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(), ["id", "name", "preview", "owner", "created", "updated"]
        )

    def test_equation_field_content(self):
        """Test that the name field has the expected content."""
        data = self.serializer.data
        self.assertEqual(data["name"], self.validated_data["name"])

    def test_parsed_equation_field_content(self):
        """Test that the owner field has the expected content."""
        data = self.serializer.data
        self.assertEqual(data["owner"], self.validated_data["owner"])

    def test_create_graph(self):
        """Test that the graph instance is created correctly."""
        serializer = GraphSerializer()
        graph = serializer.create(self.validated_data | {"name": "graph_01"})
        self.assertIsInstance(graph, Graph)
        self.assertEqual(graph.name, "graph_01")
        self.assertEqual(graph.owner, self.validated_data["owner"])

    def test_update_graph(self):
        """Test that the graph instance is updated correctly."""
        graph = Graph.objects.create(**(self.validated_data | {"name": "graph_02"}))
        serializer = GraphSerializer()
        updated_graph = serializer.update(
            graph, self.validated_data | {"name": "updated_graph"}
        )
        self.assertEqual(updated_graph.name, "updated_graph")
