import heapq
import sys
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

from graph import Graph
from heap import Heap


@dataclass
class HeapNode:
    name: int
    key: int
    parent: int

    def __init__(self, name, key, parent):
        self.name = name
        self.key = key
        self.parent = parent

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        return self.name == other.name


def build_graph(l_list: Dict[int, HeapNode]) -> Graph:
    graph: Graph = Graph(0)

    for node in l_list.values():
        if node.parent != -1:
            graph.add_edge(node.name, node.parent, node.key)
    return graph


def prim(graph: Graph, starting_node: int = 1) -> Graph:
    heap: Heap = Heap()
    heap.init_nodes(graph, starting_node)

    while not heap.is_empty():

        u: HeapNode = heap.pop()

        for n in graph.get_node_edges(u.name):

            index, tmp = heap.get(n.name)

            if tmp is not None:

                heap.remove(index)

                candidate_weight: int = graph.get_weight(u.name, tmp.name)
                if candidate_weight < tmp.key:
                    tmp.key = graph.get_weight(u.name, tmp.name)
                    tmp.parent = u.name

                heap.push(tmp)

    return build_graph(heap.nodes)
