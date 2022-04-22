from typing import List, Dict, Tuple
from graph import Edge, Graph
from union_find import UnionFindSet


def sort_edges(graph: Graph) -> List[Edge]:
    """
    Returns the list of edges of the input graph in crescent order

    Parameters
    ----------
    graph : Graph
        input graph

    Returns
    -------
    Dict[Tuple[int, int], int]:
        list of edges in crescent order
    """
    graph.static_edges.sort()
    return graph.static_edges


def kruskal_union_find(graph: Graph):
    result = []
    union_find: UnionFindSet = UnionFindSet()
    for node in graph.get_all_nodes():
        union_find.make(node)
    edges: List[Edge] = sort_edges(graph)

    for edge in edges:
        if union_find.find(edge.a) != union_find.find(edge.b):
            result.append(edge)
            union_find.union(edge.a, edge.b)
    return result
