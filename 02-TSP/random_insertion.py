import random

from circuit import Circuit
from graph import Graph


def random_insertion(graph: Graph) -> Circuit:
    """
    Returns a Circuit created using Random Insertion on the input graph
    Parameters
    ----------
    graph : Graph
        input graph

    Returns
    -------
    Circuit
        a Circuit created using Random Insertion on the input graph
    """
    #  -------- INITIALIZATION --------
    node_0 = graph.nodes[1]
    circuit = Circuit(node_0)

    min_node = None
    min_weight = None

    #  search the nearest node to node_0
    for node, weight in graph.node_weights(node_0.id):
        if min_weight is None or weight < min_weight:
            min_weight = weight
            min_node = node

    # add it to the circuit
    circuit.append(min_node, graph.weights)

    # a list of all nodes except node_0 and its nearest node
    remaining_nodes = [node_id for node_id in list(graph.nodes.keys())
                       if node_id not in [node_0.id, min_node.id]]

    # random shuffle of all nodes, doing so, we can linearly iterate over a list
    random.shuffle(remaining_nodes)

    #  -------- SELECTION --------
    for node_index in range(len(remaining_nodes)):
        # this is equal to a random choice thanks to the random shuffle
        random_node_id = remaining_nodes[node_index]

        min_delta = None
        min_node_id = 0
        for node_id, next_node_id, weight in circuit:
            # we have i and j and I want add a node k between them
            # candidate_weight = w(i, k) + w(k, j)
            candidate_weight = graph.weights[random_node_id - 1, node_id - 1] \
                               + graph.weights[random_node_id - 1, next_node_id - 1]

            # delta is the insertion cost
            delta = candidate_weight - weight

            if min_delta is None or delta < min_delta:
                # considering the min delta
                min_delta = delta
                min_node_id = node_id

        #  -------- INSERTION --------
        circuit.insert_after_node(min_node_id, random_node_id, graph.weights)

    return circuit
