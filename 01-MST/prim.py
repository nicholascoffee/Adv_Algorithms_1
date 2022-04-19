from graph import Graph
from heap import Heap, HeapNode


def prim(graph: Graph, starting_node: int = 1) -> Graph:
    heap: Heap = Heap()
    heap.init_nodes(graph, starting_node)

    while not heap.is_empty():

        u: HeapNode = heap.pop()

        for n in graph.get_node_edges(u.name):

            index, tmp = heap.get(n.name)

            if tmp is not None:

                candidate_weight: int = graph.get_weight(u.name, tmp.name)

                if candidate_weight < tmp.key:

                    tmp.key = candidate_weight
                    tmp.parent = u.name

                    heap.value_decreased(index)

    return heap.build_graph()
