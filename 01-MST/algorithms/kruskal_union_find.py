from datastructure.graph import Graph, Edges
from datastructure.union_find import UnionFindSet


def kruskal_union_find(graph: Graph) -> Graph:
    """
    Returns the Minimum Spanning Tree of the given graph using Kruskal with
    Union Find (based on union-by-size)

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
    edges: Edges = graph.get_sorted_edges()

    # Check if an edge is not inside another set, then make the union of the sets
    # and add that edge to the MST
    for edge, weight in edges.items():
        if union_find.find(edge[0]) != union_find.find(edge[1]):
            mst.add_edge(edge[0], edge[1], weight)
            union_find.union(edge[0], edge[1])
    return mst
