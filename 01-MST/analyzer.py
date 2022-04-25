import gc
import math
import os
from dataclasses import dataclass
from time import perf_counter_ns
from typing import Callable, Dict, List, Optional, Tuple
import matplotlib.pyplot as plt

from algorithms.kruskal_union_find import kruskal_union_find
from algorithms.naive_kruskal import naive_kruskal
from algorithms.prim import prim
from datastructure.graph import Graph, graph_from_file

DATASET: List[str] = sorted(os.listdir("dataset"))

# Type aliases
Time = float
DataGraph = Tuple[int, int]  # for represent only number of nodes and number of edges
MSTAlgorithm = Callable[[Graph], Graph]
ComplexityFunction = Callable[[Tuple[int, int]], Time]


def mlogn(size: Tuple[int, int]) -> float:
    return size[1] * math.log2(size[0])


def mn(size: Tuple[int, int]) -> float:
    return size[1] * size[0]


@dataclass
class Analysis:
    """
    A class for represent the data of the graph with their time execution

    Attributes
    __________
    data : DataGraph
        a tuple storing the number of nodes and edges in the graph

    time : Time
        a float representing the time of execution
    """
    data: DataGraph
    time: Time

    def __init__(self, data: Tuple[int, int], time: float):
        self.data = data
        self.time = time


def run_algorithm(graph: Graph, algorithm: MSTAlgorithm, num_calls: int) -> Time:
    """
    Execute the given MST-algorithm, over the given graph for the given number of calls,
    and return the average time of execution.

    Parameters
    ----------
    graph : graph
        is the graph in which the algorithm will be executed
    algorithm : MSTAlgorithm
        is the algorithm to execute
    num_calls : int
        number of calls that must be make

    Returns
    -------
    The average time of execution.

    """
    gc.disable()
    start_time = perf_counter_ns()

    for _ in range(num_calls):
        algorithm(graph)

    end_time = perf_counter_ns()
    gc.enable()

    return (end_time - start_time) / num_calls


def measure_time(algorithm: MSTAlgorithm, num_calls: int,
                 is_exponential: bool = False) -> List[Analysis]:
    """
    Execute the given MST-algorithm, over all the graphs in the DATASET directory for
    the given number of calls and return a sorted list of the graph and the average
    time of execution of the algorithm.

    Parameters
    ----------
    algorithm : MSTAlgorithm
        is the algorithm to execute
    num_calls : int
        number of calls that must be make
    is_exponential : bool
        Indicate if the algorithm is exponential
    Returns
    -------
    A list composed by the data of the graphs and its average time of execution of the algorithm.

    """

    # Dict where to store the data of the graphs and the average times of every execution
    times: Dict[DataGraph, List[Time]] = {}
    # Dict where to store the data of the grpahs and the average of avrage times
    avg_times: Dict[DataGraph, Time] = {}

    # Executing the algorithm over all the graphs inside the DATASET
    for file_number, file in enumerate(DATASET):

        print(str(file_number + 1) + "/68")

        graph: Graph = graph_from_file("dataset/" + file)

        # num calls decreases depending on the graph node number ^ 2
        specific_num_calls = int(num_calls / (graph.n / 2)) + 1

        if is_exponential:
            if graph.n >= 20000:
                specific_num_calls = 2
            if graph.n >= 80000:
                specific_num_calls = 1

        print("Running with: " + str(specific_num_calls))
        print()

        estimate_time: Time = run_algorithm(graph, algorithm, specific_num_calls)

        # Create the data graph to use as key in the dict
        data: DataGraph = (graph.n, graph.m)

        # Check if the data graph is already in the dict, otherwise append the time
        if data not in times:
            times[data] = []
        times[data].append(estimate_time)

    # Compute the average of all the average times for every graphs.
    # Stroing all in the dict avg_times
    for key, item in times.items():
        avg_times[key] = sum(item) / len(item)

    # Covert the dict into list for easier manuality
    analysis: List[Analysis] = []
    for key, items in avg_times.items():
        analysis.append(Analysis(data=key, time=items))
    return analysis


def plot(analysis: List[Analysis], constant: float,
         complexity_function: ComplexityFunction, algorithm_name: str,
         complexity_function_name: str, plot_numer: int = 1):
    data: Dict[int, List[float]] = {}
    avg: Dict[int, float] = {}
    references = []

    for a_item in analysis:
        n_nodes = a_item.data[0]
        if n_nodes not in data:
            data[n_nodes] = []
            references.append(constant * complexity_function(a_item.data))

        data[n_nodes].append(a_item.time)

    for key, items in data.items():
        avg[key] = sum(items) / len(items)

    times = []
    sizes = []
    for key, item in avg.items():
        times.append(item)
        sizes.append(key)
    plt.figure(plot_numer)
    plt.title(algorithm_name + " Algorithm")
    plt.plot(sizes, times, label="Our implementation")
    plt.plot(sizes, references, label=complexity_function_name)
    plt.xlabel("Node number")
    plt.ylabel("Time (ns)")
    plt.legend()


def run_analysis(algorithm: MSTAlgorithm, complexity_function: ComplexityFunction,
                 algorithm_name: str, num_calls: int = 1, is_exponential: bool = False) -> List[Analysis]:
    """
    Execute the given MST-algorithm for the given number of calls, measure the time of execution

    Parameters
    ----------
    is_exponential
    algorithm_name
    algorithm : MSTAlgorithm
        is the algorithm to execute
    complexity_function : ComplexityFunction
        is the reference function for the algorithm to be plot
    num_calls : int
        number of calls that must be make

    Returns
    -------
    List[Analysis]
        result

    """
    analysis: List[Analysis] = measure_time(algorithm, num_calls, is_exponential)
    ratios: List[Optional[float]] = [0.0]
    ratios += ([round(analysis[i + 1].time / analysis[i].time, 3)
                for i in range(len(analysis) - 1)])

    c_estimates = [round(analysis[i].time / complexity_function(analysis[i].data), 3)
                   for i in range(len(analysis))]

    with open(algorithm_name + ".csv", "w") as file:
        file.write("Nodes,Edges,Time,Constants\n")
        print("Size\t\tTime(ns)\t\t\t\tConstant\t\t\t\t\tRatio")
        print(50 * "-")

        results = []

        for index, item in enumerate(analysis):
            file.write("%d,%d,%d,%d\n" % (item.data[0], item.data[1], round(item.time, 2),
                                        c_estimates[index]))
            print(item.data, round(item.time, 2), '',
                  c_estimates[index], '', ratios[index], sep="\t\t")
            results.append((item.data, round(item.time, 2), c_estimates[index]))

        print(50 * "-")
    return analysis


def compare_plot(prim_analysis: List[Analysis], kruskal_union_find_analysis: List[Analysis],
                 naive_kruskal_analysis: List[Analysis]):
    plot(prim_analysis, 2504.639, mlogn, "Prim", " c * (m * log2(n))", 1)

    plot(kruskal_union_find_analysis, 524.839, mlogn, "Kruskal Union Find", " c * (m * log2(n))", 2)

    plot(naive_kruskal_analysis, 524.839, mn, "Naive Kruskal", "c * (m * n)", 3)

    plt.show()


def print_results():
    with open("results.csv", "w") as results_file:
        results_file.write("File,Prim,NaiveKruskal,KruskalUnionFind")
        print("Prim\t\tKruskal Union Find\t\tNaive Kruskal")
        for file in DATASET:
            graph: Graph = graph_from_file("dataset/" + file)
            results = (file, prim(graph).sum_weights(), kruskal_union_find(graph).sum_weights(),
                       naive_kruskal(graph).sum_weights())
            print("%s\t\t%d\t\t%d\t\t\t%d" % results)
            results_file.write("%s,%d,%d,%d\n" % results)
