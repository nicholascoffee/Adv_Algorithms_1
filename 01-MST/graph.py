from dataclasses import dataclass

from typing import Dict, List, TextIO, Optional

import parser

from parser import Content


@dataclass
class AdjacencyNode:
    """
    A class for representing the adjacency between two nodes and the respective weight

    Attributes
    __________
    name: int
        name of the adjacent node
    weight: int
    """
    name: int
    weight: int

    def __init__(self, name: int, weight: int):
        self.name = name
        self.weight = weight


@dataclass
class Edge:
    """
    A class for representing the edge that connect two nodes and the respective weigh

    Attributes
    __________
    a: int
        first node endpoint
    b: int
        second node endpoint
    weight: int
        the costs for travelling from a to b and vice-versa

    """

    a: int
    b: int
    weight: int

    def __init__(self, a: int, b: int, weight: int) -> None:
        self.a = a
        self.b = b
        self.weight = weight

    def __eq__(self, other):
        return ((self.a == other.a and self.b == other.b) or (self.a == other.b and self.b == other.a)) \
               and self.weight == other.weigth


@dataclass
class Graph:
    """
    A class for represent an undirected simple graph using adjacency lists

    Attributes
    __________
    adjacency_list : Dict[int, List[AdjacencyNode]]

    edges : List[Edge]

    n : int
        number of nodes in the graph

    m : int
        number of edges in the graph

    """
    adjacency_list: Dict[int, List[AdjacencyNode]]
    edges: List[Edge]

    n: int
    m: int

    def __init__(self, n: int):
        self.n = n
        self.m = 0

        self.adjacency_list = {}
        self.edges = []

    def add_edge(self, a: int, b: int, weight: int) -> None:
        """
        Add an edge to the undirected graph. If there is already an edge that connect a to b, it keeps
        only the lighter ones

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

        # check if the nodes exist in the adjacency list dictionary
        if a not in self.adjacency_list:
            self.adjacency_list[a] = []
        if b not in self.adjacency_list:
            self.adjacency_list[b] = []

        if a != b:  # since we are working with simple graphs, we do not allow self loops
            existing_edge: Edge = self.get_edge(a, b)
            if existing_edge is None:
                # there isn't any edge that already connect a to b (and vice-versa)
                # so we update both a and b adjacency nodes (since the graph is undirected)
                self.adjacency_list[a].append(AdjacencyNode(b, weight))
                self.adjacency_list[b].append(AdjacencyNode(a, weight))
                self.edges.append(Edge(a, b, weight))
                self.m += 1
            elif existing_edge.weight > weight:
                # there is an edge that connect a to b, so we just keep the lighter (based on the weight field)
                self.update_edge(a, b, weight)

    def update_edge(self, a: int, b: int, weight: int) -> None:
        """
        Update an edge in all adjacency list and edges list

        Parameters
        ----------
        a : int
            first endpoint
        b : int
            second endpoint
        weight : int
            new weight to set on the edge

        Returns
        -------
        None
        """

        # since the graph is undirected we have to update both adjacency list
        for node in self.adjacency_list[a]:
            if node.name == b:
                node.weight = weight

        for node in self.adjacency_list[b]:
            if node.name == a:
                node.weight = weight

        # now we have to update the edges list
        for edge in self.edges:
            if (edge.a == a and edge.b == b) or (edge.a == b and edge.b == a):
                edge.weight = weight

    def get_all_edges(self) -> List[Edge]:
        """
        Returns all the edges in the graph

        Returns
        -------
        List[Edge]
            list of edges in the graph
        """
        return self.edges

    def get_edge(self, a: int, b: int) -> Optional[Edge]:
        """
        Returns the Edge that connects a to b, if exists

        Parameters
        ----------
        a : int
            first endpoint
        b : int
            second endpoint

        Returns
        -------
        Edge
            Edge object that represents the link between a and b if exists, None otherwise
        """

        # since we already know the two endpoint, we can search the Edge in adjacency list
        # it is way more efficient that iterate over the edges list
        for adj_node in self.adjacency_list[a]:
            if adj_node.name == b:
                return Edge(a, b, adj_node.weight)
        return None

    def get_node_edges(self, node_name: int) -> Optional[List[AdjacencyNode]]:
        """
        Returns all adjacency nodes of a given node

        Parameters
        ----------
        node_name : int


        Returns
        -------
        List[AdjacencyNode]
            adjacency nodes of the given node if exists on the graph, None otherwise
        """
        if node_name not in self.adjacency_list:
            return None
        return self.adjacency_list[node_name]

    def get_all_nodes(self) -> Dict[int, List[AdjacencyNode]]:
        """
        Return all the nodes in the graph with their respective adjacency list

        Returns
        -------
        Dict[int, List[AdjacencyNode]]
            dictionary containing all the nodes in the graph with their respective adjacency list
        """
        return self.adjacency_list

    def get_weight(self, a: int, b: int) -> int:
        """
        Return the weight of the edge that connects a to b

        Parameters
        ----------
        a : int
            first endpoint
        b : int
            second endpoint

        Returns
        -------
        int
            weight of the edge that connects a to b

        """
        return self.get_edge(a, b).weight


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
    return _graph_from_content(parser.parse(path))


def _graph_from_content(content: Content) -> Graph:
    graph: Graph = Graph(content.n)
    for a, b, weight in content.list_triple:
        graph.add_edge(a, b, weight)

    return graph
