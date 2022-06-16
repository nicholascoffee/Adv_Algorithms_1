import os
from dataclasses import dataclass
from typing import List

from numpy import ndarray

from datastructure.heap import Heap, HeapNode
from graph import Graph, Node, graph_from_file


@dataclass
class Cut:
    graph: Graph
    s: Node
    t: Node
    value: int

    def __init__(self, graph: Graph, s: Node, t: Node):
        self.graph = graph
        self.s = s
        self.t = t
        self.value = self.__calc_value()

    def __calc_value(self):
        result = 0
        for _, weight in self.graph.adj_nodes(self.t):
            result += weight

        return result

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __str__(self):
        return "{s: %d, t: %d, value: %d}" % (self.s, self.t, self.value)


def st_min_cut(g: Graph) -> Cut:
    queue: Heap = Heap()

    queue.build_from_list(g.get_nodes())

    s, t, u = None, None, None
    while not queue.is_empty():
        u = queue.dequeue().name
        s = t
        t = u
        for v, weight in g.adj_nodes(u):
            heap_v: HeapNode = queue.get_by_name(v)
            if heap_v is not None:
                new_v_key = heap_v.key + weight
                queue.update_by_name(v, new_v_key)

    return Cut(g, s, t)


def global_min_cut_rec(g: Graph) -> Cut:
    nodes = g.get_nodes()
    if len(nodes) == 2:
        return Cut(g, nodes[0], nodes[1])

    cut1 = st_min_cut(g)

    __st_contraction(g, cut1.s, cut1.t)

    cut2 = global_min_cut_rec(g)

    if cut1 <= cut2:
        return cut1
    else:
        return cut2


def global_min_cut(g: Graph) -> int:
    return global_min_cut_rec(g).value


def __st_contraction(g: Graph, u: int, v: int) -> None:
    """
    Given a graph and two nodes inside it, the function executes a contract of those nodes.

    Parameters
    ----------
    g: Graph
        is the graph in which do the contract

    u: Node
        is the first node to be contract

    v: Node
        is the second node to be contract

    Returns
    -------
    Node

    """

    v, u = max(v, u), min(v, u)

    matrix: ndarray = g.weighted_matrix
    matrix[u][v] = matrix[v][u] = 0

    nodes: List[Node] = g.get_nodes()

    for node in nodes:
        if node != u and node != v:
            matrix[u][node] += matrix[v][node]
            matrix[node][u] += matrix[node][v]
            matrix[v][node] = matrix[node][v] = 0

    g.get_nodes().remove(v)
    g.n -= 1

if __name__ == "__main__":

    tot = 0
    files = []
    for f in os.listdir("../dataset/"):
        files.append(f)
    files.sort()

    res = ""
    graphs = []
    for f in files:
        g = graph_from_file("../dataset/" + f)
        g.name = f
        graphs.append(g)

    for g in graphs:
        rec_n = 0
        print(g.name)
        print(global_min_cut(g))