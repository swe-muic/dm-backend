"""Graph model module."""

from django.db import models


class Graph(models.Model):
    """Graph model.

    Attributes:
        name (str): The name of the graph.
        preview (str): The name of the minio bucket that stores graph preview.
        owner (str): The firebase uid of the owner of the graph.
        created (datetime): The date and time the graph was created.
        updated (datetime): The date and time the graph was last updated.
    """

    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=255)
    preview = models.CharField(max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for Graph model.

        Attributes:
            ordering (list): The ordering of the graph.
            constraints (list): The constraints of the graph
                -> one owner should not have multiple graphs under the same name.
        """

        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["name", "owner"], name="unique_graph_name")
        ]
