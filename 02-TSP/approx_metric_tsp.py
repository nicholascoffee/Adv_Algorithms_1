from MST.kruskal_union_find import kruskal_union_find
from circuit import Circuit
from graph import Graph


def approx_metric_tsp(graph: Graph) -> Circuit:
    """
    Given a graph, the function calculates the minimum Hamiltonian Cycle
    using 2-approx algorithm based on MST

    Parameters:
    -----------
    graph: Graph
        is the graph where to star finding the minimum Hamiltonian Cycle

    Returns:
    --------
    Circuit
        the circuit that represents the cycle
    """

    # start from a MST calculated on the input graph
    mst: Graph = kruskal_union_find(graph)

    # insert the nodes in the circuit using the preorder tree exploration
    return Circuit.from_mst_preorder(mst, graph.weights)


