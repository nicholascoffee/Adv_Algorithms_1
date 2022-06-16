import copy
import gc
import random
from collections import defaultdict
from sys import maxsize
from os import listdir
from time import perf_counter_ns
from math import log2
from typing import Callable, List, Dict
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
from tabulate import tabulate

from algorithms.stoer_wagner import global_min_cut
from graph import Graph, graph_from_file
from algorithms.karger_stein import recursive_contract

DATASET: List[str] = sorted(listdir("dataset"))

# Type alias
Time = float  # Union[int, float]
MinimumCutAlgorithm = Callable[[Graph], int]

ComplexityFunction = Callable[[int, int], float]


def n2logn3(n: int, m: int):
    return (n ** 2) * (log2(n) ** 3)


def mnlogn(n: int, m: int):
    return m * n * log2(n)


@dataclass
class Analysis:
    graph_name: str
    graph_n_size: int
    graph_m_size: int
    minimum_cost: int = field(default=maxsize)
    execution_time: int = field(default=maxsize)
    # Useful for Karger & Stein's analysis
    discovery_time: int = field(default=maxsize, init=False)


def measure_stoer_wagner_algorithm(name: str, g: Graph) -> Analysis:
    """

    Parameters:
    -----------
    g: Graph
        is the graph where to execute the algorithm.

    Returns:
    --------
    Analysis
    """
    result: Analysis = Analysis(name, g.n, g.m)
    min_cut = 0

    iterations = 20
    if g.n > 200:
        iterations = 5


    graph_clones = [copy.deepcopy(g) for _ in range(iterations)]

    gc.disable()
    # Start first timer
    start_execution_timer: int = perf_counter_ns()
    for i in range(iterations):
        # Execute the Karger & Stein's algorithm
        min_cut: int = global_min_cut(graph_clones[i])  # call the algorithm

    # End first timer
    end_execution_timer: int = perf_counter_ns()
    gc.enable()
    # Elaborate total execution time
    result.minimum_cost = min_cut
    result.execution_time = (end_execution_timer - start_execution_timer) / iterations
    return result


def measure_karger_stein_algorithm(name: str, g: Graph) -> Analysis:
    """
    Given a graph, the function executes log^2(n) the recursive_contract in order to have the error 
    probability less or equal 1/n.
    It returns the complete analysis of that instance problem with the discovery time.

    Parameters:
    -----------
    g: Graph
        is the graph where to execute the Karger & Stein's algorithms.

    Returns:
    --------
    Analysis
        the minimum cost, the execution time and the discovery time of that specific graph.
    """
    result: Analysis = Analysis(name, g.n, g.m)
    iterations = 20
    if g.n > 200:
        iterations = 5

    graph_clones = [copy.deepcopy(g) for _ in range(iterations)]

    gc.disable()

    # Start first timer
    start_execution_timer: int = perf_counter_ns()
    for i in range(iterations):
        for _ in range(int(log2(g.n)) ** 2):
            # Start second timer
            start_discovery_timer: int = perf_counter_ns()
            # Execute the Karger & Stein's algorithm
            min_cut: int = recursive_contract(graph_clones[i])
            # end second timer
            end_discovery_timer: int = perf_counter_ns()
            # Check if the new minimum cost is less than its previous
            if min_cut < result.minimum_cost:
                result.minimum_cost = min_cut
                result.discovery_time = end_discovery_timer - start_discovery_timer
    # End first timer
    end_execution_timer: int = perf_counter_ns()
    # Elaborate total execution time
    gc.enable()

    result.execution_time = (end_execution_timer - start_execution_timer) / iterations
    # TODO: Debug
    assert result.discovery_time <= result.execution_time
    return result


def print_comparison(karger_stein_analysis: List[Analysis], stoer_wagner_analysis: List[Analysis]):
    headers = ["Graph", "Karger Stein", "Stoer Wagner", "Equals", "Is Stoer Wagner better?"]
    data = []

    times_st_strictly_better = 0
    deltas = 0

    for ks, st in zip(karger_stein_analysis, stoer_wagner_analysis):
        if ks.minimum_cost > st.minimum_cost:
            times_st_strictly_better += 1
            deltas += ks.minimum_cost - st.minimum_cost

        data.append(
            [ks.graph_name, ks.minimum_cost, st.minimum_cost, "TRUE" if ks.minimum_cost == st.minimum_cost else "FALSE",
             "TRUE" if ks.minimum_cost >= st.minimum_cost else "FALSE"])

    table = tabulate(data, headers=headers, tablefmt="grid")
    print("Times Stoer Wagner was strictly better: " + str(times_st_strictly_better))
    print("Deltas: " + str(deltas))
    print(table)
    with open("./results/comparison.txt", "w") as f:
        f.write(str(table))
    with open("./results/comparison_data.txt", "w") as f:
        f.write("Times Stoer Wagner was strictly better: " + str(times_st_strictly_better))
        f.write("Deltas: " + str(deltas))


def analysis_study(algorithm_name: str, analysis_list: List[Analysis], complexity: ComplexityFunction):
    headers = ["Graph", "Minimum cut", "Hidden constant", "Execution time (ns)"]

    if algorithm_name == "Karger_Stein":
        headers.append("Discovery time (ns)")

    data = []
    constant = 0
    for analysis in analysis_list:
        constant = analysis.execution_time / complexity(analysis.graph_n_size, analysis.graph_m_size)

        result = [analysis.graph_name, analysis.minimum_cost, constant, analysis.execution_time]
        if algorithm_name == "Karger_Stein":
            result.append(analysis.discovery_time)

        data.append(result)

    table = tabulate(data, headers=headers, tablefmt="grid")

    with open("./results/" + algorithm_name + ".txt", "w") as f:
        f.write(str(table))

    return constant


def plot_karger_stein(analysis_list: List[Analysis], constant):
    group_times: Dict[int, List[float]] = defaultdict(list)
    avg_times: Dict[int, float] = {}
    reference_values: Dict[int, float] = {}

    for analysis in analysis_list:
        group_times[analysis.graph_n_size].append(analysis.execution_time)

    for n in group_times:
        avg_times[n] = sum(group_times[n]) / len(group_times[n])
        reference_values[n] = constant * n2logn3(n, 0)

    x = sorted(avg_times.keys())

    y_effective = []
    y_reference = []

    for n in x:
        y_effective.append(avg_times[n])
        y_reference.append(reference_values[n])

    fig = plt.figure()
    plt.title("Karger Stein Algorithm")
    plt.xlabel("Nodes")
    plt.ylabel("Time (ns)")
    plt.plot(x, y_effective, label="Effective time")
    plt.plot(x, y_reference, label="Reference time")
    plt.legend()

    plt.show()
    fig.savefig('./results/Karger_Stein.png', dpi=fig.dpi)


def plot_stoer_wagner(analysis_list: List[Analysis], constant):

    mn_group_times: Dict[(int, int), List[float]] = defaultdict(list)

    group_times: Dict[int, List[float]] = defaultdict(list)

    group_reference_times: Dict[int, List[float]] = defaultdict(list)

    avg_times: Dict[int, float] = {}
    reference_values: Dict[int, float] = {}

    for analysis in analysis_list:
        mn_group_times[analysis.graph_n_size, analysis.graph_m_size].append(analysis.execution_time)

    for n, m in mn_group_times:
        for value in mn_group_times[n, m]:
            group_reference_times[n].append(constant * mnlogn(n, m))
            group_times[n].append(value)

    for n in group_times:
        avg_times[n] = sum(group_times[n]) / len(group_times[n])
        reference_values[n] = sum(group_reference_times[n]) / len(group_reference_times[n])

    x = sorted(avg_times.keys())

    y_effective = []
    y_reference = []

    for n in x:
        y_effective.append(avg_times[n])
        y_reference.append(reference_values[n])

    fig = plt.figure()
    plt.title("Stoer Wagner Algorithm")
    plt.xlabel("Nodes")
    plt.ylabel("Time (ns)")
    plt.plot(x, y_effective, label="Effective time")
    plt.plot(x, y_reference, label="Reference time")
    plt.legend()

    plt.show()
    fig.savefig('./results/Stoer_Wagner.png', dpi=fig.dpi)


def test() -> None:
    for file_name in DATASET:
        path: str = f"./dataset/{file_name}"
        g: Graph = graph_from_file(path)
        # measure_alg(graph, algorithm, num_call)
        print(measure_karger_stein_algorithm(file_name, g))


def main():
    random.seed(0)
    karger_stein_analysis = []
    stoer_wagner_analysis = []

    for file_name in DATASET:
        path: str = f"./dataset/{file_name}"
        print("Evaluation of " + file_name)
        g: Graph = graph_from_file(path)
        if g.n > 300:
            break
        karger_stein_analysis.append(measure_karger_stein_algorithm(file_name, copy.deepcopy(g)))
        stoer_wagner_analysis.append(measure_stoer_wagner_algorithm(file_name, copy.deepcopy(g)))

    # print_comparison(karger_stein_analysis, stoer_wagner_analysis)
    ks_constant = analysis_study("Karger_Stein", karger_stein_analysis, n2logn3)
    st_constant = analysis_study("Stoer_Wagner", stoer_wagner_analysis, mnlogn)
    plot_karger_stein(karger_stein_analysis, ks_constant)
    plot_stoer_wagner(stoer_wagner_analysis, st_constant)


if __name__ == "__main__":
    main()
