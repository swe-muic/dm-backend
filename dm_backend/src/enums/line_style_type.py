"""Line style enum module."""
from enum import Enum
from typing import List, Tuple


class LineStyle(Enum):
    """
    Line style for graphing equations.

    Represented by string of line style representation
    """

    SOLID = "-"
    DASHED = "--"
    DOTTED = ":"
    DASH_DOT = "-."

    @classmethod
    def choices(cls: Enum) -> List[Tuple[str, str]]:
        """
        Return choices for enum.

        Keywork arguments:
        cls -- Enum class

        Returns:
        List of tuples of enum values and names
        """
        return [(key.value, key.name) for key in cls]
