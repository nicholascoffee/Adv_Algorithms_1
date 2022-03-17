from dataclasses import dataclass

from typing import Dict, List, TextIO


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
    n: int
    m: int

    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m

        self.nodes = {}
        for i in range(1, n + 1):
            self.nodes[i] = []

    def add_edge(self, a: int, b: int, weight: int) -> None:
        self.nodes[a].append(AdjacencyNode(b, weight))
        self.nodes[b].append(AdjacencyNode(a, weight))


def graph_from_file(filename: str) -> Graph:
    file: TextIO = open("dataset/" + filename, "r")
    n: int = int(file.readline().split()[0])

    graph: Graph = Graph(n)
    for line in file.readlines():
        data: List[str] = line.split()
        graph.add_edge(int(data[0]), int(data[1]), int(data[2]))

    return graph
