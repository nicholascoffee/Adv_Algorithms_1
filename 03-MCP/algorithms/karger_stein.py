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
