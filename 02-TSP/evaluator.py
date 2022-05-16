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
ApproximationFunction = Callable[[int], float]

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


def evaluate(algorithm: TSPAlgorithm, repetitions=200):
    file_names: List[str] = os.listdir("dataset")
    evaluations: List[Evaluation] = []

    for index, file_name in enumerate(file_names):
        graph = graph_from_file("dataset/" + file_name)
        print("Loading %s (%d/%d)" % (file_name, index + 1, len(file_names)))
        evaluations.append(__evaluate_on_dataset(algorithm, graph, repetitions))

    print("DONE\n")
    return evaluations


def prepare_data_for_plot(evaluations: List[Evaluation]):
    """
    Prepares the data for matplotlib

    """
    time_data = defaultdict(list)
    error_data = defaultdict(list)

    for evaluation in evaluations:
        time_data[evaluation.n].append(evaluation.run_time)
        error_data[evaluation.n].append(evaluation.error)

    ordered_time_data = OrderedDict(sorted(time_data.items()))
    ordered_error_data = OrderedDict(sorted(error_data.items()))

    x = []

    time_y = []
    error_y = []

    for k, v in ordered_time_data.items():
        x.append(k)
        time_y.append(sum(v) / len(v))

    for k, v in ordered_error_data.items():
        error_y.append(sum(v) / len(v) * 100)

    return x, time_y, error_y


def make_plots(random_evaluations: List[Evaluation], cheapest_evaluations: List[Evaluation],
               two_approx_evaluations: List[Evaluation]):
    random_x, random_time_y, random_error_y = prepare_data_for_plot(random_evaluations)
    cheapest_x, cheapest_time_y, cheapest_error_y = prepare_data_for_plot(cheapest_evaluations)
    two_approx_x, two_approx_time_y, two_approx_error_y = prepare_data_for_plot(two_approx_evaluations)

    #  ---- RANDOM PLOT ----
    random_time_fig = plt.figure()
    plt.title("Random Insertion run time")
    plt.plot(random_x, random_time_y)
    plt.xlabel("Node number")
    plt.ylabel("Time (ns)")
    random_time_fig.savefig("figures/random_time.png")

    random_error_fig = plt.figure()
    plt.title("Random Insertion error")
    plt.plot(random_x, random_error_y)
    plt.xlabel("Node number")
    plt.ylabel("Error (%)")
    random_error_fig.savefig("figures/random_error.png")

    #  ---- CHEAPEST PLOT ----
    cheapest_time_fig = plt.figure()
    plt.title("Cheapest Insertion run time")
    plt.plot(cheapest_x, cheapest_time_y)
    plt.xlabel("Node number")
    plt.ylabel("Time (ns)")
    cheapest_time_fig.savefig("figures/cheapest_time.png")

    cheapest_error_fig = plt.figure()
    plt.title("Cheapest Insertion error")
    plt.plot(cheapest_x, cheapest_error_y)
    plt.xlabel("Node number")
    plt.ylabel("Error (%)")
    cheapest_error_fig.savefig("figures/cheapest_error.png")

    #  ---- 2 APPROX PLOT ----
    two_approx_time_fig = plt.figure()
    plt.title("2-approx Insertion run time")
    plt.plot(two_approx_x, two_approx_time_y)
    plt.xlabel("Node number")
    plt.ylabel("Time (ns)")
    two_approx_time_fig.savefig("figures/two_approx_time.png")

    two_approx_error_fig = plt.figure()
    plt.title("2-approx Insertion error")
    plt.plot(two_approx_x, two_approx_error_y)
    plt.xlabel("Node number")
    plt.ylabel("Error (%)")
    two_approx_error_fig.savefig("figures/two_approx_error.png")

    #  ---- COMPARISON PLOT ----
    comparison_error_fig = plt.figure()
    plt.title("Comparison algorithms error")
    plt.plot(two_approx_x, random_error_y)
    plt.plot(two_approx_x, cheapest_error_y)
    plt.plot(two_approx_x, two_approx_error_y)
    plt.xlabel("Node number")
    plt.ylabel("Error (%)")
    plt.legend(["Random Insertion", "Cheapest Insertion", "2-approx"])
    comparison_error_fig.savefig("figures/comparison_error.png")


def pretty_print(evaluations: List[Evaluation], approximation_function: ApproximationFunction, name: str):
    data = []

    with open("result/" + name + ".txt", "w") as f:

        evaluations.sort(key=lambda e: e.n)

        for evaluation in evaluations:
            approx_factor = evaluation.optimal_result * approximation_function(evaluation.n)
            approx_compliant = "YES" if ((evaluation.result / evaluation.optimal_result) <= approx_factor) else "NO"
            data.append([evaluation.name, evaluation.result, evaluation.optimal_result, evaluation.error * 100,
                         approx_compliant, evaluation.run_time])

        f.write(tabulate(data, headers=["Name", "Result", "Optimal Result", "Error (%)", "Approx compliant", "Time (ns)"]))


def __evaluate_on_dataset(algorithm: TSPAlgorithm, graph: Graph, repetitions=200) -> Evaluation:
    gc.disable()
    start_time = time.perf_counter_ns()
    for i in range(repetitions):
        circuit = algorithm(graph)

    end_time = time.perf_counter_ns()
    gc.enable()

    optimal_result = __get_optimal_result(graph.name)

    return Evaluation(graph.name, graph.n, circuit.total_weight, optimal_result,
                      round((end_time - start_time) / repetitions))


def __get_optimal_result(graph_name: str):
    return __optimal_results.get(graph_name) or __optimal_results.get(graph_name[:-4])


def random_best_evaluation(repetitions: int, single_evaluation: List[Evaluation]):
    file_names: List[str] = os.listdir("dataset")
    evaluations: Dict[str, Tuple[Evaluation, int]] = {}

    for index, file_name in enumerate(file_names):
        graph = graph_from_file("dataset/" + file_name)
        print("Loading %s (%d/%d)" % (file_name, index + 1, len(file_names)))

        for i in range(repetitions):
            print("%d/%d" % (i, repetitions))
            evaluation = __evaluate_on_dataset(random_insertion, graph, 1)
            if evaluations.get(graph.name) is None:
                evaluations[graph.name] = (evaluation, 1)
            else:
                best_evaluation: Evaluation = evaluations[graph.name][0]
                if evaluation.result < best_evaluation.result:
                    evaluations[graph.name] = (evaluation, i + 1)
            if evaluation.result == evaluation.optimal_result:
                break

    random_best_data = []
    for e in evaluations.values():
        random_best_data.append(e[0])
    x, _, random_best_error = prepare_data_for_plot(random_best_data)
    _, _, random_single_error = prepare_data_for_plot(single_evaluation)

    random_comparison_fig = plt.figure()

    plt.title("Multiple run random comparison")
    plt.plot(x, random_best_error)
    plt.plot(x, random_single_error)
    plt.legend(["Best error over " + str(repetitions) + " repetitions", "Single random instance"])
    plt.xlabel("Nodes")
    plt.ylabel("Error (%)")

    random_comparison_fig.savefig("figures/random_comparison.png")

    pretty_print_random(evaluations)


def pretty_print_random(evaluations: Dict[str, Tuple[Evaluation, int]]):
    data = []

    evaluations = {k: v for k, v in sorted(evaluations.items(), key=lambda item: item[1][0].n)}

    for evaluation, i in evaluations.values():
        data.append([evaluation.name, evaluation.result, evaluation.optimal_result, evaluation.error * 100,
                     i, evaluation.run_time])

    print(tabulate(data, headers=["Name", "Result", "Optimal Result", "Error (%)", "Attempt number", "Time (ns)"]))
