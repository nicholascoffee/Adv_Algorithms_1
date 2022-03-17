from dataclasses import dataclass

from typing import Dict, List


@dataclass
class AdjacencyNode:
    name: int
    weight: int

    def __init__(self, name: int, weight: int):
        self.name = name
        self.weight = weight


@dataclass
class Graph:
    nodes: Dict[int, List[AdjacencyNode]]

    def __init__(self, n: int):
        for i in range(1, n + 1):
            self.nodes[i] = []

    def add_edge(self, a: int, b: int, weight: int) -> None:
        self.nodes[a].append(AdjacencyNode(b, weight))
        self.nodes[b].append(AdjacencyNode(a, weight))
