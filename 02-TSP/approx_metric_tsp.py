from MST.kruskal_union_find import kruskal_union_find
from circuit import Circuit
from graph import Graph


def approx_metric_tsp(graph: Graph) -> Circuit:
    mst: Graph = kruskal_union_find(graph)
    return Circuit.from_mst_preorder(mst, graph.weights)


