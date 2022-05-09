from dataclasses import dataclass
from typing import Dict, List
import numpy as np


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
    x: int
    y: int

    def __init__(self, i: int, x: int, y: int) -> None:
        self.id = i
        self.x = x
        self.y = y


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
        self.weights = np.zeros((n, n), dtype=np.int16)

    def _get_distance(self, first: Node, second: Node) -> int:
        # TODO: implement the module for calculate distance based on weigh_type
        return 1

    def add_node(self, i: int, x: int, y: int) -> None:
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

    def get_nodes(self) -> List[Node]:
        """
        Retrieve all the nodes present in the graph

        Returns
        -------
        List[Node]
            a lis of nodes that are in the graph
        """
        return list(self.nodes.values())

    def adj_nodes(self, i: int):
        for node in self.get_nodes():
            if node.id != i:
                yield node

    def calculate_weights(self) -> None:
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

    def print(self) -> None:
        """
        Print all the information of the graph
        """
        print(self.name, self.n, self.weight_type)
        for node in self.nodes:
            print(node, ":", list(self.adj_nodes(node)))
