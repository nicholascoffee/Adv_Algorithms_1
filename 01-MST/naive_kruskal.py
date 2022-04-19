from typing import List

from graph import Graph, Edge


def sort_edges(graph: Graph) -> List[Edge]:
    """
    Returns the list of edges of the input graph in crescent order

    Parameters
    ----------
    graph : Graph
        input graph

    Returns
    -------
    List[Edge]:
        list of edges in crescent order
    """
    edges: List[Edge] = graph.get_all_edges()
    edges.sort()
    return edges


def naive_kruskal(graph: Graph) -> Graph:
    """
    Returns the Minimum Spanning Tree of the given graph using Naive Kruskal Algorithm

    Parameters
    ----------
    graph : Graph
        the graph on which calculate the Minimum Spanning Tree

    Returns
    -------
    Graph :
        Minimum Spanning Tree graph based on the input graph
    """
    # empty graph to return with the solution
    mst_graph: Graph = Graph(0)

    # sorting the edges in crescent order
    edges: List[Edge] = sort_edges(graph)

    # check for all the edges sorted the nodes
    for edge in edges:
        a: int = edge.a
        b: int = edge.b
        weight: int = edge.weight

        # add in the new graph if the graph created is still acyclic,
        # else continue with the next nodes
        mst_graph.add_edge(a, b, weight)
        if mst_graph.is_cyclic(a):
            mst_graph.remove_edge(a, b)
    return mst_graph
