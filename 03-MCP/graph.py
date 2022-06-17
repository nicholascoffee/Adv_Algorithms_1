from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, Dict, List, Tuple
import numpy as np
import parser

# Type Aliases
Node = int
Edges = Dict[Tuple[Node, Node], int]

@dataclass
class Graph:
    """
    A class for represent an undirected simple graph.

    Attributes:
    -----------
    n : int
        number of nodes in the graph
    m : int
        number of edges in the graph
    nodes: List[Node]
        list containing all id of nodes inside the graph
    weighted_matrix: np.ndarray
        a matrix for store weights of edges in the graph
    weighted_degree: DefaultDict[Node, int]
        a dictionary to store the weighted degree of nodes in the graph
    """
    n: int = field(default=0)
    m: int = field(default=0)
    nodes: List[Node] = field(default_factory=lambda: list())
    # Datastructure for the algorithms of Minimum Cut
    weighted_matrix: np.ndarray = field(init=False)
    weighted_degree: DefaultDict[Node, int] = field(default_factory=lambda: defaultdict(int))

    def __post_init__(self):
        # Defer the initialization of the matrix since depends on an another field of the class
        self.weighted_matrix = np.zeros((self.n + 1, self.n + 1), dtype=int)
        self.nodes = list(range(1, self.n + 1))

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
        """
        Returns the nodes inside the graph

        Returns:
        --------
        List[Node]
            a list of nodes
        """
        return self.nodes

    def get_weight(self, a: int, b: int) -> int:
        """
        Given two nodes inside the graph, the function returns the weight
        for travelling from node a to node b if the edge exists, otherwise 
        returns 0.

        Parameters
        ----------
        a: int
            is the first node in the edge
        b: int
            is the second node in the edge
        
        Returns:
        --------
        int
            the cost for go from node a to node b
        """
        return self.weighted_matrix[a][b]

    def adj_nodes(self, node_id: int):
        """
        Given the id of a node, the function returns the adjacent nodes and their
        weights inside an iterator 

        Parameters
        ----------
        node_id: int
            is the is of the node 
        """
        for node in self.get_nodes():
            weight: int = self.weighted_matrix[node_id][node]
            if node != node_id and weight != 0:
                yield node, weight


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
