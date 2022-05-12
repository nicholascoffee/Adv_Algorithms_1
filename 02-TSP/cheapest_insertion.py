from itertools import combinations
from typing import List
from math import inf
from circuit import Circuit
from graph import Graph, Node

def _min_adjacent_node(node: Node, graph: Graph) -> Node:
    """
    """
    min_node = Node(0, 0, 0)
    min_weight = None

    #  cerco il nodo k più vicino al nodo 0
    for adjacent_node, weight in graph.node_weights(node.id):
        if min_weight is None or weight < min_weight:
            min_weight = weight
            min_node = adjacent_node
    
    return min_node

def cheapest_insertion(graph: Graph):
    """
    Given a graph, the function calculates the minimun Hamiltonian Cycle using the euristic oF Cheapest Insertion

    Parameters:
    -----------
    graph: Graph
        is thee graph where to star finding the minimun Hamiltonian Cycle

    Returns:
    --------
    Circuit
        the circuit that represents the cycle
    """
    # Starting the initialization by choosing the first node
    node_0: Node = graph.nodes[0]
    circuit: Circuit = Circuit(node_0)

    min_node: Node = _min_adjacent_node(node_0, graph)

    # Add new node in the circuit
    circuit.append(min_node, graph.weights)

    # Retriving all the nodes NOT in the circuit
    remaining_nodes: List[int] = [node_id for node_id in list(graph.nodes.keys())
                       if node_id not in [node_0.id, min_node.id]]

    # Cycling all the nodes in the circuit, and one on one adding them in the circuit
    while not len(remaining_nodes) == 0:
        # Create all the pair representing edges in the partial circuit
        pairs = list(combinations(circuit.circuit_nodes.keys(), 2))
        
        min_weight: int = int(inf)
        id_predecessor_node = 0
        id_candidate_node: int = 0

        # For all the nodes not in the circuit
        for id_new_node in remaining_nodes:
            # For all the possible combinations of edges in the partial circuit
            for id_i, id_j in pairs:
                # Calculate the cost of adding the new_node in the partial circuit
                candidate_weight: int = graph.get_weight(id_i, id_new_node) + graph.get_weight(id_new_node, id_j) - graph.get_weight(id_i, id_j)
                # If this cost is less of the previous one, save it and save the node and his predecessor
                if candidate_weight < min_weight:
                    min_weight = candidate_weight
                    id_predecessor_node = id_i
                    id_candidate_node = id_new_node
        # Insertion of the new node in the circuit
        circuit.insert_after_node(id_predecessor_node, id_candidate_node, graph.weights)
        # Remove the node of the circuit from the list of non nodes in circuit
        remaining_nodes.remove(id_candidate_node)

    return circuit