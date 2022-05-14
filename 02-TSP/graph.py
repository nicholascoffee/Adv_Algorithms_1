from dataclasses import dataclass
from typing import Dict, List, Tuple

from node import Node
from parser import parse, Content
import distances as dst
import numpy as np

Edges = Dict[Tuple[int, int], int]


@dataclass
class Graph:
    """
    Dataclass for represent a graph of nodes.

    Attributes
    ----------
    name: str
        the name of the graph for more readable reference for optimal solution
    n: int
        the total number of nodes in the graph
    weight_type: str
        the type of representation of the nodes. Useful to know how to calculate distance between nodes
    nodes: Dict[int, Node]
        a list to store all the nodes present in the graph
    weights: np.ndarray
        a matrix to store all the weight for go from one node to another one in the graph
    """
    name: str
    n: int
    weight_type: str
    # Store all the nodes to access more quickly
    nodes: Dict[int, Node]
    # Store the weights of alle the edges in a matrix
    weights: np.ndarray

    def __init__(self, name: str, n: int, weight_type: str) -> None:
        self.name = name
        self.n = n
        self.weight_type = weight_type
        self.nodes = {}
        self.weights = np.zeros((n, n))

    def _get_distance(self, first: Node, second: Node) -> int:
        """
        Given two nodes, the function returns the distance calculate baesd on
        the variable "weight_type" of the graph

        Attributes:
        -----------
        first: Node
            node from calculate the distance
        second: Node
            node to calculate the distance

        Returns:
        int
            the distance between two nodes
        """
        distance: int = 0
        if self.weight_type == "EUC_2D":
            distance = dst.get_distance_euclidean(first.x, first.y, second.x, second.y)
        elif self.weight_type == "GEO":
            distance = dst.get_distance_geographic(first.x, first.y, second.x, second.y)
        return distance

    def add_node(self, i: int, x: float, y: float) -> None:
        """
        Insert a new node in the graph with specific attributes

        Parameters
        ----------
        i: int
            is the identifier for the new node
        x: int
            is the latitude coordinate for the new node
        y: int
            is the longitude coordinate for the new node
        """
        # Insert new node in the list of all nodes in the graph
        self.nodes[i] = Node(i, x, y)
        if len(self.nodes) == self.n:
            self._calculate_weights()

    def get_nodes(self) -> List[Node]:
        """
        Retrieve all the nodes present in the graph

        Returns
        -------
        List[Node]
            a lis of nodes that are in the graph
        """
        return list(self.nodes.values())

    def adj_nodes(self, node_id: int):
        for node in self.get_nodes():
            if node.id != node_id:
                yield node

    def node_weights(self, node_id: int):
        for node in self.get_nodes():
            if node.id != node_id:
                yield node, self.weights[node_id - 1, node.id - 1]

    def _calculate_weights(self) -> None:
        """
        Calculate all the distance in the nodes inside the graph.
        MUST BE USE ONLY WHEN THE GRAPH IS COMPLETE.
        """
        # Considering every node in the graph
        for node in self.nodes.values():
            # and considering all the other nodes
            for adj_node in self.adj_nodes(node.id):
                # Calculate the distance between the nodes and store the result in the matrix
                # Indexes start from 0, but nodes start from 1
                self.weights[node.id - 1, adj_node.id - 1] = self._get_distance(node, adj_node)

    def get_weight(self, first_node_id: int, second_node_id: int) -> int:
        """
        Given the ids of two nodes, the function returns the cost to go from one to the other

        Parameters:
        -----------
        first_node_id: int
            is the id of the node to go from
        second_node_id: int
            is the id of the node to go to

        Returns:
        --------
        int:
            the weight of the traverselling
        """
        return self.weights[first_node_id - 1][second_node_id - 1]

    def print(self) -> None:
        """
        Print all the information of the graph
        """
        print(self.name, self.n, self.weight_type)
        print(self.nodes)
        print(self.weights)

    def get_all_nodes(self) -> List[int]:
        return list(self.nodes.keys())

    def get_sorted_edges(self) -> Edges:
        edges = dict()

        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                edges[i, j] = self.get_weight(i, j)

        return {k: v for k, v in sorted(edges.items(), key=lambda item: item[1])}

    def update_edge(self, node1, node2, weight):

        self.weights[node1 - 1, node2 - 1] = weight  # TODO commenta
        self.weights[node2 - 1, node1 - 1] = weight




def graph_from_file(path: str) -> Graph:
    """
    Given the path to a ".tsp" file, the funtion return the corresponding graph

    Attributes:
    -----------
    path: str
        the path to the file which contains the information of the graph

    Returns:
    --------
    Graph
        the corresponding graph
    """
    content: Content = parse(path)
    graph: Graph = Graph(content.name, content.n, content.weight_type)
    for i, x, y in content.triples:
        graph.add_node(i, x, y)
    return graph
