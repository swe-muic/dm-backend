from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from dm_backend.src.models.graph import Graph
from dm_backend.tests.baker_recipes.graph_baker_recipe import graph_recipe
from dm_backend.tests.baker_recipes.user_baker_recipe import user_recipe


class GraphAPIViewSetTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/viewset/graphs/"
        self.url_id = lambda equation_id: f"{self.url}{equation_id}/"
        self.owner = user_recipe.make(username="test_user")
        self.valid_payload = {
            "name": "test_graph",
            "owner": self.owner.id,
        }

    def test_get_all_graphs_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(len(response.data), 0)

    def test_get_all_graphs(self):
        graph = graph_recipe.make(**self.valid_payload | {"owner": self.owner})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], graph.id)

    def test_get_graph(self):
        graph = graph_recipe.make(**self.valid_payload | {"owner": self.owner})
        response = self.client.get(self.url_id(graph.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(response.data["name"], graph.name)

    def test_get_nonexistent_graph(self):
        response = self.client.get(self.url_id(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "fail")
        self.assertEqual(response.data["detail"], "Not found.")

    def test_create_graph(self):
        response = self.client.post(self.url, self.valid_payload)
        graph = Graph.objects.first()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(Graph.objects.count(), 1)
        self.assertEqual(graph.name, self.valid_payload["name"])

    def test_create_invalid_graph(self):
        payload = self.valid_payload | {"name": ""}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "fail")
        self.assertEqual(Graph.objects.count(), 0)

    def test_update_graph(self):
        graph = graph_recipe.make(**self.valid_payload | {"owner": self.owner})
        payload = self.valid_payload | {"name": "updated_graph"}
        response = self.client.put(self.url_id(graph.id), payload)
        graph = Graph.objects.filter(id=graph.id).first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["message"], "success")
        self.assertEqual(graph.name, payload["name"])

    def test_update_nonexistent_graph(self):
        payload = self.valid_payload | {"name": "updated_graph"}
        response = self.client.put(self.url_id(999), payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "fail")
        self.assertEqual(response.data["detail"], "Not found.")

    def test_update_invalid_graph(self):
        graph = graph_recipe.make(**self.valid_payload | {"owner": self.owner})
        payload = self.valid_payload | {"name": ""}
        response = self.client.put(self.url_id(graph.id), payload)
        graph = Graph.objects.filter(id=graph.id).first()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "fail")
        self.assertEqual(graph.name, self.valid_payload["name"])

    def test_delete_graph(self):
        graph = graph_recipe.make(**self.valid_payload | {"owner": self.owner})
        response = self.client.delete(self.url_id(graph.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Graph.objects.filter(id=graph.id).exists())
        self.assertEqual(Graph.objects.count(), 0)

    def test_delete_nonexistent_graph(self):
        response = self.client.delete(self.url_id(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()["message"], "fail")
        self.assertEqual(response.data["detail"], "Not found.")
