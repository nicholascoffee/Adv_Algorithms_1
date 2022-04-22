import heapq
import sys
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

from graph import Graph


@dataclass
class HeapNode:
    name: int
    key: int
    index: int
    parent: int

    def __init__(self, name, key=0, parent=0):
        self.name = name
        self.key = key
        self.parent = parent
        self.index = -1

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __eq__(self, other):
        return self.name == other.name


def _left(index: int) -> int:
    return index * 2 + 1


def _right(index: int) -> int:
    return index * 2 + 2


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

        for index, heap_node in enumerate(self.nodes.values()):
            self.push(heap_node)

    def sift_up(self, node_index):
        if node_index == 0:
            return
        parent: int = _parent(node_index)
        while node_index > 0 and self.heap[parent] > self.heap[node_index]:
            self.swap(node_index, parent)
            node_index = parent
            if node_index != 0:
                parent: int = _parent(node_index)

    def sift_down(self, node_index):
        left_index = _left(node_index)
        while left_index < self.size():
            minimum_child_index = self.get_min_child_index(node_index)
            if self.heap[node_index] > self.heap[minimum_child_index]:
                self.swap(node_index, minimum_child_index)
            else:
                return
            node_index = minimum_child_index
            left_index = _left(node_index)

    def size(self) -> int:
        return len(self.heap)

    def last_index(self):
        return self.size() - 1

    def swap(self, index1, index2):
        self.heap[index1].index = index2
        self.heap[index2].index = index1
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def push(self, node: HeapNode):
        self.heap.append(node)
        node.index = self.last_index()
        self.sift_up(self.last_index())

    def get(self, node_index: int) -> HeapNode:
        return self.heap[node_index]

    def get_by_name(self, node_name: int) -> Optional[HeapNode]:

        node: HeapNode = self.nodes[node_name]
        if node.index > self.last_index():
            return None
        else:
            return node

    def get_min_child_index(self, node_index: int) -> int:

        left_index = _left(node_index)

        if left_index > self.last_index():
            # Nessun figlio
            raise Exception("No child")

        if left_index == self.last_index():
            return left_index  # unico figlio

        right_index = _right(node_index)

        if self.heap[left_index] < self.heap[right_index]:
            return left_index
        else:
            return right_index

    def pop(self) -> HeapNode:
        if self.is_empty():
            raise Exception("Heap empty")

        min_node = self.heap[0]

        self.swap(0, self.last_index())

        self.heap.pop()

        self.sift_down(0)

        return min_node

    def update(self, node_index: int, new_key: int):
        old_key = self.heap[node_index].key
        self.heap[node_index].key = new_key

        if old_key > new_key:
            self.sift_up(node_index)
        elif old_key < new_key:
            self.sift_down(node_index)

    def build_graph(self) -> Graph:
        graph: Graph = Graph(0)

        for node in self.nodes.values():
            if node.parent != -1:
                graph.add_edge(node.name, node.parent, node.key)
        return graph
