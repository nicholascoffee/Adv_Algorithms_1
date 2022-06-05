from collections import defaultdict
from copy import deepcopy
from random import randrange
from typing import Dict, List, Tuple, DefaultDict
from graph import Graph, Node
from numpy import ndarray
from math import sqrt

# TODO: Big refactor of the two function called cumulative_weighted_array since
# they do the same thing but with different implementation

def __cumulative_weighted_array(weighted_dict: Dict[Node, int]) -> Dict[Node, int]:
    """
    Given a dictionary of nodes and weighted degrees, the function returns a dictionary of nodes with
    the cumulative degree. In details, C[k] = sum[from i to k]D[i]
    """
    cumulative_dict: Dict[Node, int] = defaultdict(int)
    for node, degree in weighted_dict.items():
        if node == 1:
            cumulative_dict[node] += degree
        else:
            cumulative_dict[node] += (degree + cumulative_dict[node - 1])
    return cumulative_dict

def __cumulative_weighted_array2(weighted_adjacency_list: List[Node]) -> Dict[Node, int]:
    cumulative_dictionary: Dict[Node, int] = defaultdict(int)
    index: Node = 1
    # Avoid the first value since is always zero, so starting from second element
    for weight in weighted_adjacency_list[1:]:
        if index == 1:
            cumulative_dictionary[index] += weight
        else:
            cumulative_dictionary[index] += (weight + cumulative_dictionary[index - 1])
        index += 1
    return cumulative_dictionary

def __binary_search(values: List[Node], r: int) -> Node:
    """
    Given a list of nodes and a value r, the function uses the binary search to find an index i
    such that values[i - 1] <= r < values[i]. Starts with 1 as first position.

    Parameters
    ----------
    values: List[Node]
        list of values where to find the index i

    r: int
        is the value against which to look for the index i 

    Returns
    -------
    Node
        the index (id) of the node which resepct the property
    """
    pivot: Node = len(values) // 2
    if (len(values) <= 1):
        return pivot + 1
    if (r >= values[pivot - 1] and r < values[pivot]):
        return pivot + 1
    elif r < values[pivot - 1]:
        return __binary_search(values[:pivot], r)
    else: # r > values[pivot]
        return (pivot + __binary_search(values[pivot:], r))

def __random_select(cumulative_dict: Dict[Node, int]) -> Node:
    """
    Given a cumulative dictionary of weights, the function generates a random integer
    r such that 0 <= r < cumulative_dict[last-value] and use it to find a good node for
    the cut.

    Parameters
    ----------
    cumulative_dict: Dict[Node, int]
        is a dictionary of cumulative weights from which start finding the node 

    Returns
    -------
    Node
        the id of the node for the cut in the graph
    """
    # Take a random value from 0 to the last value of the cumulative dictionary
    last_value: int = list(cumulative_dict.values())[-1]
    r: Node = randrange(last_value)
    u: Node = __binary_search(list(cumulative_dict.values()), r)
    return u

def __edge_select(g: Graph) -> Tuple[Node, Node]:
    """
    Given a graph, the function returns a pair of nodes which represents a good minimun cut.

    Parameters
    ----------
    g: Graph
        is the graph where to find the nodes for the cut

    Returns
    -------
    Tuple[Node, Node]
        is the pair of nodes (i.e. the edge) good for the minuimun cut
    """
    # Build cumulative weights array on weighted degree
    c1: Dict[Node, int] = __cumulative_weighted_array(g.weighted_degree)
    u: Node = __random_select(c1)
    c2: Dict[Node, int] = __cumulative_weighted_array2(g.weighted_matrix[u])
    v: Node = __random_select(c2)
    # TODO: Assertion for avoid self-loop or non existing edges
    assert (v != u) and (g.get_weight(u, v) != 0), "Self-Loop or Not Existing Edge returned"
    return u, v

def __contract_edge(g: Graph, u: Node, v: Node) -> None:
    """
    Given a graph and two nodes inside it, the function executes a contract of those nodes.

    Parameters
    ----------
    g: Graph
        is the graph in which do the contract

    u: Node
        is the first node to be contract

    v: Node
        is the second node to be contract

    Returns
    -------
    Node

    """
    matrix: ndarray = g.weighted_matrix
    degree: DefaultDict[Node, int] = g.weighted_degree
    degree[u] = degree[u] + degree[v] + (2 * g.get_weight(u, v))
    degree[v] = 0
    matrix[u][v] = matrix[v][u] = 0
    nodes: List[Node] = g.get_nodes()
    for node in nodes:
        if node != u and node != v:
            matrix[u][node] += matrix[v][node]
            matrix[node][u] += matrix[node][v]
            matrix[v][node] = matrix[node][v] = 0
    g.n -= 1

def __contract(g: Graph, k: int) -> Graph:
    """
    Given a graph and an integer k, the function executes k times the contraction 
    of nodes inside the graph.

    Parameters
    ----------
    g: Graph
        is the graph where execute k times the contraction

    k: int
        is the number of contractions 

    Returns
    -------
    Graph
        the graph after k contractions
    """
    n: int = g.n
    # TODO: is n-k include in the iterations?
    for _ in range(n - k):
        u, v = __edge_select(g)
        __contract_edge(g, u, v)
    return g
