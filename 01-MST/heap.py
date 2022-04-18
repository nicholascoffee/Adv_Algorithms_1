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

    def __eq__(self, other):
        return self.name == other.name


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

    def remove(self, i: int):
        self.heap[i] = self.heap[-1]
        self.heap.pop()
        if i < len(self.heap):
            heapq._siftup(self.heap, i)
            heapq._siftdown(self.heap, 0, i)
