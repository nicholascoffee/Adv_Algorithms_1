from dataclasses import dataclass

from typing import Dict, List, Optional, Tuple

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
        return ((self.a == other.a and self.b == other.b)
                or (self.a == other.b and self.b == other.a)) and self.weight == other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def connect(self, a: int, b: int) -> bool:
        return (self.a == a and self.b == b) or (self.a == b and self.b == a)


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

    def __init__(self, n: int = 0, m: int = 0):
        self.n = n
        self.m = m

        self.adjacency_list = {}
        self.edges = []

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

        # check if the nodes exist in the adjacency list dictionary
        if a not in self.adjacency_list:
            self.adjacency_list[a] = []
            self.n += 1
        if b not in self.adjacency_list:
            self.adjacency_list[b] = []
            self.n += 1

        if a != b:  # since we are working with simple graphs, we do not allow self loops
            existing_edge: Optional[Edge] = self.get_edge(a, b)
            if existing_edge is None:
                # there isn't any edge that already connect a to b (and vice-versa)
                # so we update both a and b adjacency nodes (since the graph is undirected)
                self.adjacency_list[a].append(AdjacencyNode(b, weight))
                self.adjacency_list[b].append(AdjacencyNode(a, weight))
                self.edges.append(Edge(a, b, weight))
                self.m += 1
            elif existing_edge.weight > weight:
                # there is an edge that connect a to b, so we just keep the lighter
                # (based on the weight field)
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

    def remove_edge(self, a: int, b: int):  # TODO fix
        """
        Removes an edge from the graph

        Parameters
        ----------
        a : int
            first node name
        b :
            second node name

        """
        a_adj_list = self.get_node_edges(a)
        b_adj_list = self.get_node_edges(b)

        for a_index, a_node in enumerate(a_adj_list):
            if a_node.name == b:
                del a_adj_list[a_index]
                break
        for b_index, b_node in enumerate(b_adj_list):
            if b_node.name == a:
                del b_adj_list[b_index]
                break
        for e_index, edge in enumerate(self.edges):
            if edge.connect(a, b):
                del self.edges[e_index]
                break

    def get_node_edges(self, node_name: int) -> List[AdjacencyNode]:
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
            raise Exception("Node not found")
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
        edge: Optional[Edge] = self.get_edge(a, b)
        if edge is None:
            raise Exception("Edge not found")

        return edge.weight

    def is_cyclic(self, starting_node: int) -> bool:
        """
        Returns true if the graph is cyclic, otherwise false

        Parameters
        ----------
        starting_node : int
            the node name on which start the analysis

        Returns
        -------
        bool
            if the graph is cyclic or not
        """
        visited_nodes: Dict[int, bool] = {}
        visited_edges: Dict[Tuple[int, int], bool] = {}
        nodes_to_visit: List[int] = [starting_node]  # nodes to visit in CURRENT level

        while len(nodes_to_visit) > 0:
            future_level: List[int] = []
            for node_name in nodes_to_visit:
                adj_nodes: List[AdjacencyNode] = self.get_node_edges(node_name)

                if visited_nodes.get(node_name):
                    return True  # non è ciclico

                visited_nodes[node_name] = True

                for adj_node in adj_nodes:  # per ogni nodo adiacente
                    if not visited_edges.get((node_name, adj_node.name)):
                        # non ho mai attraversato questo arco
                        # (essendo un grafo non diretto ne ho 2 per ogni coppia)
                        # li metto entrambi per non dover controllare gli opposti ogni volta
                        visited_edges[(adj_node.name, node_name)] = True
                        # sono arrivato ad un nodo da un arco mai visitato, se è davvero ciclico,
                        # non dovrei averlo già visitato
                        future_level.append(adj_node.name)

                nodes_to_visit = future_level
        return False

    def sum_weights(self) -> int:
        """
        Returns the sum of all edges

        Returns
        -------
        int
            sum of all edges
        """
        result: int = 0
        for edge in self.get_all_edges():
            result += edge.weight
        return result

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
    graph: Graph = Graph()
    for a, b, weight in content.list_triple:
        graph.add_edge(a, b, weight)

    return graph
