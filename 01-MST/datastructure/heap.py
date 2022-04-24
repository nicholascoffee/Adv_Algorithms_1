import sys
from dataclasses import dataclass
from typing import List, Dict, Optional
from datastructure.graph import Graph


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

    def __ge__(self, other):
        return self.key >= other.key

    def __eq__(self, other):
        return self.name == other.name


def _left(index: int) -> int:
    """
    Returns the left child index of the input index
    Parameters
    ----------
    index : int
        input index

    Returns
    -------
    int
        index of the left child
    """
    return index * 2 + 1


def _right(index: int) -> int:
    """
    Returns the right child index of the input index
    Parameters
    ----------
    index : int
        input index

    Returns
    -------
    int
        index of the right child
    """
    return index * 2 + 2


def _parent(index: int) -> int:
    """
    Returns the parent node index of the input index
    Parameters
    ----------
    index : int
        input index

    Returns
    -------
    int
        index of the parent node
    """
    return (index - 1) // 2


@dataclass
class Heap:
    heap: List[HeapNode]
    nodes: Dict[int, HeapNode]
    indexes: Dict[int, int]

    def __init__(self):
        self.heap = []
        self.nodes = {}
        self.indexes = {}

    def init_nodes(self, graph: Graph, starting_node: int):
        for node in graph.get_all_nodes():
            self.nodes[node] = HeapNode(node, sys.maxsize, -1)

        self.nodes[starting_node].key = 0

        for heap_node in self.nodes.values():
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
        """
        Swap 2 nodes updating the indexes' dictionary
        Parameters
        ----------
        index1
        index2

        """
        self.indexes[self.heap[index1].name] = index2
        self.indexes[self.heap[index2].name] = index1

        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def push(self, node: HeapNode):
        """
        Add a node in the heap
        Parameters
        ----------
        node : HeapNode
            input node

        """
        self.heap.append(node)
        self.indexes[node.name] = self.last_index()
        self.sift_up(self.last_index())

    def get(self, node_index: int) -> HeapNode:
        return self.heap[node_index]

    def get_by_name(self, node_name: int) -> Optional[HeapNode]:
        """
        Returns a HeapNode (if exists) by its name
        Parameters
        ----------
        node_name : str

        Returns
        -------

        """
        node: HeapNode = self.nodes[node_name]
        if self.indexes[node_name] > self.last_index():
            return None

        return node

    def get_min_child_index(self, node_index: int) -> int:
        """
        Returns the index of the minimum child of a given node
        Parameters
        ----------
        node_index : int
            input node

        Returns
        -------
        Minimum child of the input node
        """
        left_index = _left(node_index)

        if left_index > self.last_index():
            # Nessun figlio
            raise Exception("No child")

        if left_index == self.last_index():
            return left_index  # unico figlio

        right_index = _right(node_index)

        if self.heap[left_index] < self.heap[right_index]:
            return left_index

        return right_index

    def pop(self) -> HeapNode:
        """
        Returns the minimum node in the heap and removes it from the heap
        Returns
        -------
        HeapNode
            minimum node in the heap
        """
        if self.is_empty():
            raise Exception("Heap empty")

        min_node = self.heap[0]

        self.swap(0, self.last_index())

        self.heap.pop()

        self.sift_down(0)

        return min_node

    def update(self, node_index: int, new_key: int):
        """
        Updates the key of a given node index
        Parameters
        ----------
        node_index
        new_key

        """
        old_key = self.heap[node_index].key
        self.heap[node_index].key = new_key

        if old_key > new_key:
            self.sift_up(node_index)
        elif old_key < new_key:
            self.sift_down(node_index)

    def build_graph(self) -> Graph:
        """
        Returns a Graph object from the heap

        Returns
        -------
        Graph
            the resulting graph

        """
        graph: Graph = Graph(0)

        for node in self.nodes.values():
            if node.parent != -1:
                graph.add_edge(node.name, node.parent, node.key)
        return graph
