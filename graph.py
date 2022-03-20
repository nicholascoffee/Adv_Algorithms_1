from dataclasses import dataclass

from typing import Dict, List, TextIO, Optional


@dataclass
class AdjacencyNode:
    name: int
    weight: int

    def __init__(self, name: int, weight: int):
        self.name = name
        self.weight = weight


@dataclass
class Edge:
    a: int
    b: int
    weight: int

    def __init__(self, a: int, b: int, weight: int) -> None:
        self.a = a
        self.b = b
        self.weight = weight


@dataclass
class Graph:
    adjacency_list: Dict[int, List[AdjacencyNode]]

    # TODO campo ridondante
    # valutare se abbia senso mantenere una lista di archi nonostante si possa ottenere dinamicamente
    # inoltre non credo che mantenere questo campo sia corretto per l'implementazione "liste di adiacenza"
    edges: List[Edge]

    n: int
    m: int

    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m

        self.adjacency_list = {}
        self.edges = []

    def add_edge(self, a: int, b: int, weight: int) -> None:
        if a not in self.adjacency_list:
            self.adjacency_list[a] = []
        if b not in self.adjacency_list:
            self.adjacency_list[b] = []

        # no self loops
        if a != b:
            self.adjacency_list[a].append(AdjacencyNode(b, weight))
            self.adjacency_list[b].append(AdjacencyNode(a, weight))

            if self.get_edge(a, b) is None:
                self.edges.append(Edge(a, b, weight))

    def get_all_edges(self) -> List[Edge]:
        return self.edges

    def get_edge(self, a: int, b: int) -> Optional[Edge]:
        for adj_node in self.adjacency_list[a]:
            if adj_node.name == b:
                return Edge(a, b, adj_node.weight)
        return None

    # get all arcs of given node
    def get_node_edges(self, node_name: int) -> Optional[List[AdjacencyNode]]:
        if node_name not in self.adjacency_list:
            return None
        return self.adjacency_list[node_name]

    def get_all_nodes(self) -> Dict[int, List[AdjacencyNode]]:
        return self.adjacency_list

    def get_weight(self, a: int, b: int) -> int:
        return self.get_edge(a, b).weight


def graph_from_file(filename: str) -> Graph:
    file: TextIO = open("dataset/" + filename, "r")
    first_line_data: List[str] = file.readline().split()
    n: int = int(first_line_data[0])
    m: int = int(first_line_data[1])

    graph: Graph = Graph(n, m)
    for line in file.readlines():
        data: List[str] = line.split()
        graph.add_edge(int(data[0]), int(data[1]), int(data[2]))

    file.close()
    return graph
