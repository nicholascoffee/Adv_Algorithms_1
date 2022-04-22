import gc
import os
from dataclasses import dataclass
from time import perf_counter_ns, perf_counter
from typing import Callable, Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import numpy as np

from graph import Graph, graph_from_file


@dataclass
class Analysis:
    size: Tuple[int, int]
    time: float

    def __init__(self, size: Tuple[int, int], time: float):
        self.size = size
        self.time = time


MSTAlgorithm = Callable[[Graph], Graph]
ComplexityFunction = Callable[[Tuple[int, int]], float]


def run_algorithm(graph: Graph, algorithm: MSTAlgorithm, num_calls: int) -> float:
    gc.disable()
    start_time = perf_counter_ns()

    for _ in range(num_calls):
        algorithm(graph)

    end_time = perf_counter_ns()
    gc.enable()

    return (end_time - start_time) / num_calls


def measure_run_times(algorithm: MSTAlgorithm, num_calls: int) -> List[Analysis]:
    data: Dict[Tuple[int, int], List[float]] = {}

    files: List[str] = os.listdir("dataset")
    files.sort()
    print(files)
    for i, file in enumerate(files):
        if i > 40:  # TODO rimuovi il blocco
            continue
        print("init " + file)
        graph: Graph = graph_from_file("dataset/" + file)
        estimate_time = run_algorithm(graph, algorithm, num_calls)

        size: Tuple[int, int] = (graph.n, graph.m)

        if size not in data:
            data[size] = []

        data[size].append(estimate_time)

    avg_results: Dict[Tuple[int, int], float] = {}
    for key, item in data.items():
        print(item)
        avg_results[key] = sum(item) / len(item)

    analysis: List[Analysis] = []

    for key, value in avg_results.items():
        analysis.append(Analysis(key, value))

    analysis.sort(key=lambda it: it.size[0])

    return analysis


def plot(analysis: List[Analysis]):
    # TODO schifo
    d: Dict[int, List[float]] = {}
    avg: Dict[int, float] = {}
    references = []

    for a in analysis:
        n_nodes = a.size[0]
        if n_nodes not in d:
            d[n_nodes] = []
            references.append(2558.177 * a.size[1] * np.log2(n_nodes))

        d[n_nodes].append(a.time)

    for key, items in d.items():
        avg[key] = sum(items)/len(items)

    times = []
    sizes = []
    for key, item in avg.items():
        times.append(item)
        sizes.append(key)
    plt.plot(sizes, times)
    plt.plot(sizes, references)
    plt.show()


def run_analysis(algorithm: MSTAlgorithm, complexity_function: ComplexityFunction,
                 num_calls: int = 1):
    analysis: List[Analysis] = measure_run_times(algorithm, num_calls)

    ratios: List[Optional[float]] = [0.0] + \
                                    [round(analysis[i + 1].time / analysis[i].time, 3) for i in
                                     range(len(analysis) - 1)]

    c_estimates = [round(analysis[i].time / complexity_function(analysis[i].size), 3)
                   for i in range(len(analysis))]

    print("Size\t\tTime(ns)\t\t\t\tConstant\t\t\t\t\tRatio")
    print(50 * "-")
    for index, item in enumerate(analysis):
        print(item.size, round(item.time, 2), '',
              c_estimates[index], '', ratios[index], sep="\t\t")

    print(50 * "-")
    plot(analysis)
