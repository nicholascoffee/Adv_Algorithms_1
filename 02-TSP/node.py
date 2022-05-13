from dataclasses import dataclass


@dataclass
class Node:
    """
    Dataclass for represent a node inside a graph.

    Attributes
    ----------
    i: int
        the identifier for the node. Must be unique
    x: int
        the latitude coordinate of the node
    y: int
        the longitude coordinate of the node

    """
    id: int
    x: float
    y: float

    def __init__(self, i: int, x: float, y: float) -> None:
        self.id = i
        self.x = x
        self.y = y
