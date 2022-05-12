import parser
from graph import Graph
from random_insertion import random_insertion


def main():
    content = parser.parse("dataset/burma14.tsp")
    graph = Graph(content.name, content.n, content.weight_type)

    for n, x, y in content.triples:
        graph.add_node(n, x, y)
    graph.calculate_weights()

    print(graph.weights)

    circuit = random_insertion(graph)

    print(circuit.total_weight)

    for from_i, to_i, w in circuit:
        print("%d  -- %d --> " % (from_i, w))

if __name__ == '__main__':
    main()
