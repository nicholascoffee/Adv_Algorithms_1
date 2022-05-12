import random

from circuit import Circuit
from graph import Graph


def random_insertion(graph: Graph):
    #  -------- INITIALIZATION --------
    node_0 = graph.nodes[1]
    circuit = Circuit(node_0)

    min_node = None
    min_weight = None

    #  cerco il nodo k più vicino al nodo 0
    for node, weight in graph.node_weights(node_0.id):
        if min_weight is None or weight < min_weight:
            min_weight = weight
            min_node = node

    # lo aggiungo al circuito
    circuit.append(min_node, graph.weights)

    # prendo tutti i nodi, tranne 0 e k
    remaining_nodes = [node_id for node_id in list(graph.nodes.keys())
                       if node_id not in [node_0.id, min_node.id]]

    # li mescolo a caso, così dopo posso scorrere la lista linearmente
    random.shuffle(remaining_nodes)

    #  -------- SELECTION --------
    for node_index in range(len(remaining_nodes)):
        # dato che ho fatto una shuffle, scorro linearmente la lista per avere nodi casuali
        random_node_id = remaining_nodes[node_index]

        min_delta = None
        min_node_id = 0
        for node_id, next_node_id, weight in circuit:
            # ora ho node_id e next_node_id collegati da un weight.
            # Io devo aggiungere un nodo k tra node_id e next_node_id
            # candidate weight è il peso (da node_id a k) + (da k a next_node_id)
            candidate_weight = graph.weights[random_node_id - 1, node_id - 1] \
                               + graph.weights[random_node_id - 1, next_node_id - 1]

            # calcolo quanto peso mi aggiunge al circuito e prendo il più piccolo
            delta = candidate_weight - weight

            if min_delta is None or delta < min_delta:
                min_delta = delta
                min_node_id = node_id

        #  -------- INSERTION --------
        # ora min_node_id è il nodo a cui devo appendere il mio nodo per minimizzare il peso aggiuntivo
        circuit.insert_after_node(min_node_id, random_node_id, graph.weights)

    return circuit
