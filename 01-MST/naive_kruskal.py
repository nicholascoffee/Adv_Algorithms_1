from typing import List, Dict, Tuple

from graph import Graph, Edge


def sort_edges(graph: Graph) -> Dict[Tuple[int, int], int]:
    """
    Returns the list of edges of the input graph in crescent order

    Parameters
    ----------
    graph : Graph
        input graph

    Returns
    -------
    Dict[Tuple[int, int], int]:
        dict of edges in crescent order
    """
    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    return dict(sorted(graph.get_all_edges().items(), key=lambda item: item[1]))


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
    mst_graph: Graph = Graph()

    # sorting the edges in crescent order
    edges: Dict[Tuple[int, int], int] = sort_edges(graph)

    # check for all the edges sorted the nodes
    for edge, weight in edges.items():
        # add in the new graph if the graph created is still acyclic,
        # else continue with the next nodes
        mst_graph.add_edge(edge[0], edge[1], weight)
        if mst_graph.is_cyclic(edge[0]):
            mst_graph.remove_edge(edge[0], edge[1])
    return mst_graph
