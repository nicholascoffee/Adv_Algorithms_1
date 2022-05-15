from dataclasses import dataclass
from typing import Dict

import numpy as np

from graph import Graph
from node import Node


@dataclass
class CircuitNode:
    """
    Class for represent a node in a Circuit

    id : int
        node identifier
    next : CircuitNode
        next node in the circuit
    next_weight : int
        the cost to go from the current node to the next one
    """

    id: int
    next: 'CircuitNode'
    next_weight: int

    def __init__(self, i: int, next_node: 'CircuitNode' = None, next_weight: int = 0):
        self.id = i
        self.next = next_node
        self.next_weight = next_weight


@dataclass
class Circuit:
    start_node: CircuitNode
    end_node: CircuitNode
    circuit_nodes: Dict[int, CircuitNode]
    total_weight: int

    def __init__(self, starting_node: Node):
        self.start_node = CircuitNode(starting_node.id)
        self.start_node.next = self.start_node
        self.circuit_nodes = {starting_node.id: self.start_node}
        self.total_weight = 0
        self.end_node = self.start_node

    def is_in_circuit(self, node_id: int) -> bool:
        return node_id in self.circuit_nodes

    def append(self, node: Node, weights: np.array):
        """
        Add a new node at the end of the circuit
        Parameters
        ----------
        node: Node
            node to add
        weights: np.array
            weights of the graph


        """
        # TODO commenta perchè nodo start, perche il next è lo start
        if node.id == self.end_node.id:
            return

        new_node = CircuitNode(node.id, self.start_node, weights[node.id - 1, self.start_node.id - 1])
        self.total_weight += new_node.next_weight

        self.total_weight -= self.end_node.next_weight

        self.end_node.next = new_node

        self.end_node.next_weight = weights[self.end_node.id - 1, new_node.id - 1]

        self.total_weight += self.end_node.next_weight

        self.circuit_nodes[new_node.id] = new_node

        self.end_node = new_node

    def insert_after_node(self, from_node_id: int, to_new_node_id: int, weights: np.array):
        """
        Insert a new circuit after a node in the circuit

        Parameters
        ----------
        from_node_id: int
            the node already in the circuit in which append the new node
        to_new_node: Node
            the node to insert in the circuit after from_node
        weights:
            all the weight in the graph

        """

        # Retrieve the CircuitNode from a Node object
        current_node = self.circuit_nodes[from_node_id]
        # Store the current next node in a variable
        current_next_node = current_node.next

        # Create the new node as a CircuitNode
        new_next_node = CircuitNode(to_new_node_id)

        # Insert the new node after the given node and update next_weight and total_weight
        self.total_weight -= current_node.next_weight
        current_node.next = new_next_node
        current_node.next_weight = weights[current_node.id - 1, new_next_node.id - 1]
        self.total_weight += current_node.next_weight

        # The new node has the old next node as its own next node but with a different weight
        new_next_node.next = current_next_node
        new_next_node.next_weight = weights[new_next_node.id - 1, current_next_node.id - 1]
        self.total_weight += new_next_node.next_weight

        # Insert the new CircuitNode in the dictionary
        self.circuit_nodes[new_next_node.id] = new_next_node

        if self.start_node == self.end_node or current_node == self.end_node:
            self.end_node = new_next_node

    def __iter__(self):
        yield self.start_node.id, self.start_node.next.id, self.start_node.next_weight
        nav = self.start_node.next

        while nav != self.start_node:
            yield nav.id, nav.next.id, nav.next_weight
            nav = nav.next

    @staticmethod
    def from_mst_preorder(mst: Graph, weights: np.array) -> 'Circuit':
        starting_node: Node = mst.nodes[1]
        circuit: Circuit = Circuit(starting_node)
        Circuit.__preorder(mst, starting_node.id, circuit, weights)
        return circuit

    @staticmethod
    def __preorder(mst: Graph, node_id: int, circuit: 'Circuit', weights) -> None:
        #  inizio subito a vedere node_id
        circuit.append(mst.nodes[node_id], weights)

        children = []

        # ora devo vedere i figli
        for adj_node, weight in mst.node_weights(node_id):
            adj_node_id = adj_node.id
            if weight != 0 and not circuit.is_in_circuit(adj_node_id):
                children.append((adj_node_id, weight))
        children.sort(key=lambda i: i[1])

        for child in children:
            Circuit.__preorder(mst, child[0], circuit, weights)
