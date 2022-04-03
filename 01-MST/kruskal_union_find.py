from typing import List, Set
from graph import Edge, Graph
from union_find import UnionFindSet

def kruskalUnfionFind(graph: Graph) -> Set[Edge]:
    A: Set[Edge] = set()
    UF: UnionFindSet = UnionFindSet()
    for node in graph.get_all_nodes().keys():
        UF.make(node)
    edges: List[Edge] = graph.get_all_edges().sort(key=lambda e: e.weight)
    for edge in edges:
        if (UF.find(edge.a) != UF.find(edge.b)):
            A.add(edge)
            UF.union(edge.a, edge.b)
    return A
