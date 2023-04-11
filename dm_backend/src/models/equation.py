"""Equation model module."""

from django.db import models

from dm_backend.src.enums.line_style_type import LineStyle


class Equation(models.Model):
    """Equation model.

    Attributes:
        equation (str): The equation to be parsed (input by the user).
        parsed_equation (str): The parsed equation (represented by the graph).
        color (int): The color of the equation (represented in decimal).
        line_style (str): The line style of the equation.
        graph (Graph): The graph that the equation belongs to.
        line_width (int): The line width of the equation.
    """

    equation = models.CharField(max_length=100)
    parsed_equation = models.CharField(max_length=100)
    color = models.IntegerField()
    line_style = models.CharField(
        max_length=8, choices=LineStyle.choices(), default=LineStyle.SOLID.value
    )
    graph = models.ForeignKey("Graph", on_delete=models.CASCADE)
    line_width = models.IntegerField()
