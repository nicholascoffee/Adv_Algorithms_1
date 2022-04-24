from datastructure.graph import Graph
from datastructure.heap import Heap, HeapNode


def prim(graph: Graph, starting_node: int = 1) -> Graph:
    """
    Returns the MST of the inout graph
    Parameters
    ----------
    graph : Graph
        the input graph
    starting_node : int
        Prim require a starting node

    Returns
    -------
    Graph
        minimum spanning tree graph of the input graph
    """
    heap: Heap = Heap()
    heap.init_nodes(graph, starting_node)

    while not heap.is_empty():

        # since we are using a Heap, pop() always returns the minimum node (based on the key)
        min_node: HeapNode = heap.pop()

        for adjacency_node_name in graph.get_node_edges(min_node.name):

            # from the node's name, we obtain the HeapNode object
            adjacency_node = heap.get_by_name(adjacency_node_name)

            if adjacency_node is not None:
                # we update adjacency_node's key only if we found a better weight
                candidate_weight: int = graph.get_weight(min_node.name, adjacency_node.name)

                if candidate_weight < adjacency_node.key:
                    adjacency_node.parent = min_node.name
                    heap.update(heap.indexes[adjacency_node.name], candidate_weight)

    return heap.build_graph()
