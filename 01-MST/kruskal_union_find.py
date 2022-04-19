from typing import List
from graph import Edge, Graph
from union_find import UnionFindSet


def build_graph(edges: List[Edge]) -> Graph:
    graph: Graph = Graph(0)
    for edge in edges:
        graph.add_edge(edge.a, edge.b, edge.weight)
    return graph


def kruskalUnionFind(graph: Graph) -> Graph:
    result: List[Edge] = []
    union_find: UnionFindSet = UnionFindSet()
    for node in graph.get_all_nodes().keys():
        union_find.make(node)
    edges: List[Edge] = graph.get_all_edges()
    edges.sort(key=lambda e: e.weight)
    for edge in edges:
        if union_find.find(edge.a) != union_find.find(edge.b):
            result.append(edge)
            union_find.union(edge.a, edge.b)
    return build_graph(result)
