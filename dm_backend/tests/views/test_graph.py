from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from dm_backend.src.models.graph import Graph
from dm_backend.tests.baker_recipes.graph_baker_recipe import graph_recipe
from dm_backend.tests.baker_recipes.user_baker_recipe import user_recipe


class GraphAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_url = "/api/graphs/"
        self.update_url = lambda graph_id: f"/api/graphs/{graph_id}/"
        self.delete_url = lambda graph_id: f"/api/graphs/{graph_id}/"
        self.owner = user_recipe.make(username="test_user")
        self.valid_payload = {
            "name": "test_graph",
            "owner": self.owner.id,
        }

    def test_create_graph(self):
        response = self.client.post(self.create_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Graph.objects.count(), 1)
        graph = Graph.objects.first()
        self.assertEqual(graph.name, self.valid_payload["name"])

    def test_create_invalid_graph(self):
        data = self.valid_payload | {"name": ""}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_graph(self):
        graph = graph_recipe.make(**self.valid_payload | {"owner": self.owner})
        data = self.valid_payload | {"name": "updated_graph"}
        response = self.client.put(self.update_url(graph.id), data)
        graph = Graph.objects.filter(id=graph.id).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(graph.name, data["name"])

    def test_update_nonexistent_graph(self):
        data = self.valid_payload | {"name": "updated_graph"}
        response = self.client.put(self.update_url(999), data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invalid_graph(self):
        graph = graph_recipe.make(**self.valid_payload | {"owner": self.owner})
        data = self.valid_payload | {"name": ""}
        response = self.client.put(self.update_url(graph.id), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_graph(self):
        graph = graph_recipe.make(**self.valid_payload | {"owner": self.owner})
        response = self.client.delete(self.delete_url(graph.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Graph.objects.filter(id=graph.id).exists())

    def test_delete_nonexistent_graph(self):
        response = self.client.delete(self.delete_url(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue("does not exist" in response.json()["detail"])
