from datastructure.graph import Graph, Edges


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
    edges: Edges = graph.get_sorted_edges()

    # check for all the edges sorted the nodes
    for edge, weight in edges.items():
        # add in the new graph if the graph created is still acyclic,
        # else continue with the next nodes
        mst_graph.add_edge(edge[0], edge[1], weight)
        if mst_graph.is_cyclic(edge[0]):
            mst_graph.remove_edge(edge[0], edge[1])
    return mst_graph
