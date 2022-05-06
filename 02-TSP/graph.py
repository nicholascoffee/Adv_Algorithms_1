from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Dict, List
import numpy as np

@dataclass
class Node:
    """
    Dataclass for rappresent a node inside a graph.

    Attributes
    ----------
    id: int
        the identifier for the node. Must be unique
    x: int
        the latitude coordinate of the node
    y: int
        the longitude coordinate of the node

    """
    id: int
    x: int
    y: int

    def __init__(self, id: int, x: int, y: int) -> None:
        self.id = id
        self.x = x
        self.y = y

@dataclass
class Graph:
    """
    Dataclass for rappresent a graph of nodes.

    Attributes
    ----------
    name: str
        the name of the graph for more readdable reference for optimal solution
    n: int
        the total number of nodes in the graph
    weight_type: str
        the type of representation of the nodes. Useful to know how to calculate distance between nodes
    adjacency_list: DefaultDict[int, List[Node]]
        a dict to store all the adjancent nodes respect to a specific node
    nodes: Dict[int, Node]
        a list to store all the nodes present in the graph
    weights: np.ndarray
        a matrix to store all the weight for go from one node to another one in the graph
    """
    name: str
    n: int
    weight_type: str
    # Map all the neighbors of the nodes in the graph
    # TODO: Is it necessary? Can we use only the nodes attribute?
    adjacency_list: DefaultDict[int, List[Node]]
    # Store all the nodes to access more quickly
    nodes: Dict[int, Node]
    # Store the weights of alle the edges in a matrix
    weights: np.ndarray

    def __init__(self, name: str, n: int, weight_type: str) -> None:
        self.name = name
        self.n = n
        self.weight_type = weight_type
        self.adjacency_list = defaultdict(list)
        self.nodes = {}
        self.weights = np.zeros((n, n), dtype=np.int16)

    def _get_distance(self, first: Node, second: Node) -> int:
        # TODO: implement the module for calculate distance based on weigth_type
        return 1

    def add_node(self, id: int, x: int, y: int) -> None:
        """
        Insert a new node in the graph with sepcific attributes

        Parameters
        ----------
        id: int
            is the identifier for the new node
        x: int
            is the latitude coordinate for the new node
        y: int
            is the longitude coordinate for the new node
        """
        new_node: Node = Node(id, x, y)
        nodes: Dict[int, Node] = self.nodes
        adj: DefaultDict[int, List[Node]] = self.adjacency_list

        # Add the new node to all adjacency lists of the other nodes
        for list_node in adj.values():
            list_node.append(new_node)

        # Add all the other nodes to the adjacency list of the new node
        adj[id] = list(nodes.values())
        # Insert new node in the list of all nodes in the graph
        nodes[id] = new_node

    def get_nodes(self) -> List[Node]:
        """
        Retrive all the nodes present in the graph

        Returns
        -------
        List[Node]
            a lis of nodes that are in the graph
        """
        return list(self.nodes.values())

    def get_adj_nodes(self, id: int) -> List[Node]:
        """
        Retrive all the adajcent nodes of a node

        Parameters
        ----------
        id: int
            the identifier of the node of which the neighboors are searched

        Returns
        -------
        List[Node]
            a lis of nodes that are in the graph
        """
        return self.adjacency_list[id]

    def calculate_weights(self) -> None:
        """
        Calcute all the distance in the nodes inside the graph.
        MUST BE USE ONLY WHEN THE GRAPH IS COMPLETE.S
        """
        # Considering evrey node in the graph
        for node in self.nodes.values():
            # and considering all the other nodes
            for adj_node in self.get_adj_nodes(node.id):
                # Calculate the distance between the nodes and store the result in the matrix
                # Indexes start from 0, but nodes start from 1
                self.weights[node.id - 1, adj_node.id - 1] = self._get_distance(node, adj_node)

    def print(self) -> None:
        """
        Print all the infromations of the graph
        """
        print(self.name, self.n, self.weight_type)
        for node, list_node in self.adjacency_list.items():
            print(node, ":", list_node)
