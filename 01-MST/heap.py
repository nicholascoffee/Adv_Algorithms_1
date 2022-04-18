import heapq
import sys
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

from graph import Graph


@dataclass
class HeapNode:
    name: int
    key: int
    parent: int

    def __init__(self, name, key=0, parent=0):
        self.name = name
        self.key = key
        self.parent = parent

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __eq__(self, other):
        return self.name == other.name


def _parent(index: int) -> int:
    return (index - 1) // 2


@dataclass
class Heap:
    heap: List[HeapNode]
    nodes: Dict[int, HeapNode]

    def __init__(self):
        self.heap = []
        self.nodes = {}

    def init_nodes(self, graph: Graph, starting_node: int):
        for node in graph.get_all_nodes():
            self.nodes[node] = HeapNode(node, sys.maxsize, -1)

        self.nodes[starting_node].key = 0

        for heap_node in self.nodes.values():
            heapq.heappush(self.heap, heap_node)

    # heapq.heapify(self.heap)

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def push(self, node):
        heapq.heappush(self.heap, node)

    def pop(self) -> HeapNode:
        return heapq.heappop(self.heap)

    def get(self, node_name: int) -> Tuple[int, Optional[HeapNode]]:

        index: int = -1

        for pos, node in enumerate(self.heap):
            if node.name == node_name:
                index = pos
                break

        if index == -1:
            return -1, None
        else:
            return index, self.heap[index]

    def value_decreased(self, index):
        if index == 0:
            return

        parent: int = _parent(index)
        # alread changed, need balance, sono SICURO che il
        while index > 0 and self.heap[parent] > self.heap[index]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            if index != 0:
                parent: int = _parent(index)

    def build_graph(self) -> Graph:
        graph: Graph = Graph(0)

        for node in self.nodes.values():
            if node.parent != -1:
                graph.add_edge(node.name, node.parent, node.key)
        return graph
