from typing import List
from datastructure.graph import Edge, Graph
from datastructure.union_find import UnionFindSet

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

def kruskal_union_find(graph: Graph) -> Graph:
    """
    Returns the Minimum Spanning Tree of the given graph using Kruskal with Union Find (based on union-by-size)

    Parameters
    ----------
    graph : Graph
        the graph on which calculate the Minimum Spanning Tree

    Returns
    -------
    Graph :
        Minimum Spanning Tree graph based on the input graph
    """
    mst: Graph = Graph()
    union_find: UnionFindSet = UnionFindSet()

    # Create all the initial sets of union-find
    for node in graph.get_all_nodes():
        union_find.make(node)
    
    # Sort the edges of the graph
    edges: List[Edge] = sort_edges(graph)

    # Check if an edge is not inside anthor set, then make the union of the sets
    # and add that edge to the MST
    for edge in edges:
        if union_find.find(edge.a) != union_find.find(edge.b):
            mst.add_edge(edge.a, edge.b, edge.weight)
            union_find.union(edge.a, edge.b)
    return mst
