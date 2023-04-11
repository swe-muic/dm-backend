from django.test import TestCase

from dm_backend.tests.baker_recipes.graph_baker_recipe import graph_recipe


class TestGraph(TestCase):
    def test_create_graph(self):
        graph_name = "graph1"
        graph = graph_recipe.make(name=graph_name)
        self.assertEqual(graph.name, graph_name)

    def test_create_graph_with_owner(self):
        owner_uid = "firebase_uid"
        graph = graph_recipe.make(owner=owner_uid)
        self.assertEqual(graph.owner, owner_uid)

    def test_create_graph_with_preview(self):
        preview = "preview_minio_bucket_name"
        graph = graph_recipe.make(preview=preview)
        self.assertEqual(graph.preview, preview)
