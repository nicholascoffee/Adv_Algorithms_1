from typing import List

from graph import Graph, Edge


def sorted_edges(graph: Graph) -> List[Edge]:
    edges = graph.get_all_edges()
    edges.sort()
    return edges


def naive_kruskal(graph: Graph) -> Graph:
    # empty graph to return with the solution

    A: graph = Graph(0)
    i = 0
    # sorting the edges in crescent order

    edges = sorted_edges(graph)

    # check for all the edges sorted the nodes
    for e in edges:
        a = edges[i].a
        b = edges[i].b
        weight = edges[i].weight

        # add in the new graph if the graph created is still acyclic, else continue with the next ndoes

        A.add_edge(a, b, weight)
        if A.is_cyclic(a):
            A.remove_edge(a, b)
        i = i + 1
    return A
