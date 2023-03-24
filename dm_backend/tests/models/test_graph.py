from django.test import TestCase

from dm_backend.tests.baker_recipes.graph_baker_recipe import graph_recipe
from dm_backend.tests.baker_recipes.user_baker_recipe import user_recipe


class TestGraph(TestCase):
    def test_create_graph(self):
        graph_name = "graph1"
        graph = graph_recipe.make(name=graph_name)
        self.assertEqual(graph.name, graph_name)

    def test_create_graph_with_owner(self):
        owner_name = "owner1"
        owner = user_recipe.make(username=owner_name)
        graph = graph_recipe.make(owner=owner)
        self.assertEqual(graph.owner.username, owner_name)

    def test_create_graph_with_preview(self):
        preview = "preview_minio_bucket_name"
        graph = graph_recipe.make(preview=preview)
        self.assertEqual(graph.preview, preview)
