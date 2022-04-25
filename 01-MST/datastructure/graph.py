from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import parser
from parser import Content

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
    adjacency_list: Dict[int, Dict[int, int]]
    edges: Edges

    n: int
    m: int

    def __init__(self, n: int = 0, m: int = 0):
        self.n = n
        self.m = m

        self.adjacency_list = {}
        self.edges = {}

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
            self.adjacency_list[a] = {}
            self.n += 1
        if b not in self.adjacency_list:
            self.adjacency_list[b] = {}
            self.n += 1

        if a != b:  # since we are working with simple graphs, we do not allow self loops
            already_existing_weight: int = self.get_weight(a, b)
            if already_existing_weight is None:
                # there isn't any edge that already connect a to b (and vice-versa)
                # so we update both a and b adjacency nodes (since the graph is undirected)
                self.adjacency_list[a][b] = weight
                self.adjacency_list[b][a] = weight

                self.edges[(a, b)] = weight

                self.m += 1
            elif already_existing_weight > weight:
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
        self.adjacency_list[a][b] = weight
        self.adjacency_list[b][a] = weight

        self.edges[(a, b)] = weight

    def get_all_edges(self) -> Edges:
        """
        Returns all the edges in the graph

        Returns
        -------
        Dict[Tuple[int, int], int]
            list of edges in the graph
        """
        return self.edges

    def remove_edge(self, a: int, b: int):
        """
        Removes an edge from the graph

        Parameters
        ----------
        a : int
            first node name
        b :
            second node name

        """
        self.get_node_edges(a).pop(b)
        self.get_node_edges(b).pop(a)
        del self.edges[(a, b)]

    def get_node_edges(self, node_name: int) -> Dict[int, int]:
        """
        Returns all adjacency nodes of a given node

        Parameters
        ----------
        node_name : int


        Returns
        -------
        Dict[int, int]
            adjacency nodes of the given node if exists on the graph, None otherwise
        """
        if node_name not in self.adjacency_list:
            raise Exception("Node not found")
        return self.adjacency_list[node_name]

    def get_all_nodes(self) -> Dict[int, Dict[int, int]]:
        """
        Return all the nodes in the graph with their respective adjacency list

        Returns
        -------
        Dict[int, Dict[int, int]]:
            dictionary containing all the nodes in the graph with their respective adjacency list
        """
        return self.adjacency_list

    def get_weight(self, a: int, b: int) -> Optional[int]:
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
        return self.adjacency_list[a].get(b)

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
                if visited_nodes.get(node_name):
                    return True  # è ciclico

                visited_nodes[node_name] = True

                adj_nodes = self.get_node_edges(node_name)
                for adj_node in adj_nodes:  # per ogni nodo adiacente
                    if not visited_edges.get((node_name, adj_node)):
                        # non ho mai attraversato questo arco
                        # (essendo un grafo non diretto ne ho 2 per ogni coppia)
                        # li metto entrambi per non dover controllare gli opposti ogni volta
                        visited_edges[(adj_node, node_name)] = True
                        # visited_edges[(node_name, adj_node)] = True
                        # sono arrivato ad un nodo da un arco mai visitato, se è davvero ciclico,
                        # non dovrei averlo già visitato
                        future_level.append(adj_node)

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
        for weight in self.get_all_edges().values():
            result += weight
        return result

    def get_sorted_edges(self) -> Edges:
        """
        Returns the list of edges of the input graph in crescent order

        Returns
        -------
        Dict[Tuple[int, int], int]:
            dict of edges in crescent order
        """
        # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
        return dict(sorted(self.get_all_edges().items(), key=lambda item: item[1]))


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
