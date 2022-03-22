import heapq
import sys
from dataclasses import dataclass
from typing import List, Dict

from graph import Graph


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


def build_graph(l: Dict[int, HeapNode]) -> Graph:
    graph: Graph = Graph(0)

    for node in l.values():
        if node.parent != -1:
            graph.add_edge(node.name, node.parent, node.key)
    return graph


def prim(graph: Graph, starting_node: int) -> Graph:
    nodes: Dict[int, HeapNode] = {}
    heap: List[HeapNode] = []

    for node in graph.get_all_nodes():
        nodes[node] = HeapNode(node, sys.maxsize, -1)

    nodes[starting_node].key = 0

    for node in nodes.values():
        heapq.heappush(heap, node)

    while len(heap) != 0:
        heapq.heapify(heap)
        u: HeapNode = heapq.heappop(heap)

        for node in graph.get_node_edges(u.name):

            if node in heap:
                tmp: HeapNode = nodes[node.name]

                heap.remove(tmp)

                candidate_weight: int = graph.get_weight(u.name, tmp.name)
                if candidate_weight < tmp.key:
                    tmp.key = graph.get_weight(u.name, tmp.name)
                    tmp.parent = u.name

                heapq.heappush(heap, tmp)
    return build_graph(nodes)
