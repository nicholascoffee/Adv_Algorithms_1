from datastructure.graph import Graph
from datastructure.heap import Heap, HeapNode

def prim(graph: Graph, starting_node: int = 1) -> Graph:
    heap: Heap = Heap()
    heap.init_nodes(graph, starting_node)

    while not heap.is_empty():

        u: HeapNode = heap.pop()

        for n in graph.get_node_edges(u.name):

            tmp = heap.get_by_name(n)

            if tmp is not None:
                candidate_weight: int = graph.get_weight(u.name, tmp.name)

                if candidate_weight < tmp.key:
                    tmp.parent = u.name
                    heap.update(tmp.index, candidate_weight)

    return heap.build_graph()
