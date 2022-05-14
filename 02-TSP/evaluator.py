import gc
import os
import time
from collections import defaultdict, OrderedDict
from dataclasses import dataclass
from typing import Callable, List, Dict, Tuple

from tabulate import tabulate

from circuit import Circuit
from graph import Graph, graph_from_file
import matplotlib.pyplot as plt

from random_insertion import random_insertion

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

    evaluations.sort(key=lambda e: e.n)

    for evaluation in evaluations:
        data.append([evaluation.name, evaluation.result, evaluation.optimal_result, evaluation.error * 100,
                     evaluation.run_time])

    print(tabulate(data, headers=["Name", "Result", "Optimal Result", "Error (%)", "Time (ns)"]))


def __evaluate_on_dataset(algorithm: TSPAlgorithm, graph: Graph, repetitions=1) -> Evaluation:
    gc.disable()
    start_time = time.perf_counter_ns()
    for _ in range(repetitions):
        circuit = algorithm(graph)

    end_time = time.perf_counter_ns()
    gc.enable()

    optimal_result = __get_optimal_result(graph.name)

    return Evaluation(graph.name, graph.n, circuit.total_weight, optimal_result,
                      round((end_time - start_time) / repetitions))


def __get_optimal_result(graph_name: str):
    return __optimal_results.get(graph_name) or __optimal_results.get(graph_name[:-4])


def random_best_evaluation(repetitions: int):
    file_names: List[str] = os.listdir("dataset")
    evaluations: Dict[str, Tuple[Evaluation, int]] = {}

    for index, file_name in enumerate(file_names):
        graph = graph_from_file("dataset/" + file_name)
        print("Loading %s (%d/%d)" % (file_name, index + 1, len(file_names)))

        for i in range(repetitions):
            evaluation = __evaluate_on_dataset(random_insertion, graph)
            if evaluations.get(graph.name) is None:
                evaluations[graph.name] = (evaluation, 1)
            else:
                best_evaluation: Evaluation = evaluations[graph.name][0]
                if evaluation.result < best_evaluation.result:
                    evaluations[graph.name] = (evaluation, i + 1)
            if evaluation.result == evaluation.optimal_result:
                break

    pretty_print_random(evaluations)


def pretty_print_random(evaluations: Dict[str, Tuple[Evaluation, int]]):
    data = []

    evaluations = {k: v for k, v in sorted(evaluations.items(), key=lambda item: item[1][0].n)}

    for evaluation, i in evaluations.values():
        data.append([evaluation.name, evaluation.result, evaluation.optimal_result, evaluation.error * 100,
                     i, evaluation.run_time])

    print(tabulate(data, headers=["Name", "Result", "Optimal Result", "Error (%)", "Attempt number", "Time (ns)"]))
