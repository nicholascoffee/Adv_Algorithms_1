from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, Dict, List, Optional, Tuple
import numpy as np
import parser

Node = int
Edges = Dict[Tuple[Node, Node], int]

@dataclass
class Graph:
    """
    A class for represent an undirected simple graph using adjacency lists

    Attributes
    __________
    adjacency_list : Dict[int, List[AdjacencyNode]]

    edges : Edges

    n : int
        number of nodes in the graph
    m : int
        number of edges in the graph

    """
    n: int = field(default=0)
    m: int = field(default=0)
    # TODO: we nedd edges?
    # edges: Edges = field(default_factory=dict)
    # Datastructure for the algorithms of Minimun Cut
    weighted_matrix: np.ndarray = field(init=False)
    weighted_degree: DefaultDict[Node, int] = field(default_factory=lambda: defaultdict(int))

    def __post_init__(self):
        # Defer the initialization of the matrix since depends on an another field of the class
        self.weighted_matrix = np.zeros((self.n + 1, self.n + 1), dtype=int)

    def add_edge(self, a: int, b: int, weight: int) -> None:
        """
        Add an edge to the undirected graph.
        If there is already an edge that connect a to b, it keeps only the lighter ones

        Parameters
        ----------
        a : int
            first edge endpoint
        b : int
            second edge endpoint
        weight : int
            the cost to travel from a to b and vice-versa

        Returns
        -------
        None

        """
        # Get refernce to the interl datastructure of the grpah
        matrix: np.ndarray = self.weighted_matrix
        degree: DefaultDict[Node, int] = self.weighted_degree
        # Add the new weight into the matrix
        matrix[a][b] = matrix[b][a] = weight
        # Update the weighted degree of the two nodes
        degree[a] += weight
        degree[b] += weight

    def get_nodes(self) -> List[Node]:
        # Big Cheat: getting nodes from keys of the dict of weighted degree
        return self.weighted_degree.keys()

    def get_weight(self, a: int, b: int) -> int:
        return self.weighted_matrix[a][b]

def graph_from_file(path: str) -> Graph:
    """
    Load the graph from a file

    Parameters
    ----------
    path : str
        the relative or absolute path to the input source file

    Returns
    -------
    Graph
        the graph built based on the file content

    """
    content: parser.Content = parser.parse(path)
    graph: Graph = Graph(content.n, content.m)
    for triple in content.list_triple:
        graph.add_edge(triple[0], triple[1], triple[2])
    return graph
