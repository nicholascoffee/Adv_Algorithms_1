import gc
import os
import time
from collections import defaultdict, OrderedDict
from dataclasses import dataclass
from typing import Callable, List

from tabulate import tabulate

from circuit import Circuit
from graph import Graph, graph_from_file
import matplotlib.pyplot as plt

TSPAlgorithm = Callable[[Graph], Circuit]

__optimal_results = {
    "burma14": 3323,
    "ulysses16": 6859,
    "ulysses22": 7013,
    "eil51": 426,
    "berlin52": 7542,
    "kroD100": 21294,
    "kroA100": 21282,
    "ch150": 6528,
    "gr202": 40160,
    "gr229": 134602,
    "pcb442": 50778,
    "d493": 35002,
    "dsj1000": 18659688
}


@dataclass
class Evaluation:
    name: str
    n: int
    result: float
    optimal_result: float
    error: float
    run_time: int

    def __init__(self, name, n: int, result, optimal_result, run_time: int):
        self.name = name
        self.n = n
        self.result = result
        self.optimal_result = optimal_result
        self.run_time = run_time
        self.error = (result - optimal_result) / optimal_result


def evaluate(algorithm: TSPAlgorithm):
    file_names: List[str] = os.listdir("dataset")
    evaluations: List[Evaluation] = []

    for index, file_name in enumerate(file_names):
        graph = graph_from_file("dataset/" + file_name)
        print("Loading %s (%d/%d)" % (file_name, index + 1, len(file_names)))
        evaluations.append(__evaluate_on_dataset(algorithm, graph))

    pretty_print(evaluations)

    show_plot(evaluations)


def show_plot(evaluations: List[Evaluation]):
    evaluations.sort(key=lambda e: e.n)
    data = defaultdict(list)

    for evaluation in evaluations:
        data[evaluation.n].append(evaluation.run_time)

    ordered_data = OrderedDict(sorted(data.items()))

    x = []
    y = []

    for k, v in ordered_data.items():
        x.append(k)
        y.append(sum(v) / len(v))

    plt.plot(x, y)
    plt.show()


def pretty_print(evaluations: List[Evaluation]):
    data = []
    for evaluation in evaluations:
        data.append([evaluation.name, evaluation.result, evaluation.optimal_result, evaluation.error * 100,
                     evaluation.run_time])

    print(tabulate(data, headers=["Name", "Result", "Optimal Result", "Error (%)", "Time (ns)"]))


def __evaluate_on_dataset(algorithm: TSPAlgorithm, graph: Graph) -> Evaluation:
    repetitions = 20
    gc.disable()
    start_time = time.perf_counter_ns()
    for _ in range(repetitions):
        circuit = algorithm(graph)

    end_time = time.perf_counter_ns()
    gc.enable()

    optimal_result = __optimal_results.get(graph.name) or __optimal_results.get(graph.name[:-4])

    return Evaluation(graph.name, graph.n, circuit.total_weight, optimal_result,
                      round((end_time - start_time) / repetitions))
