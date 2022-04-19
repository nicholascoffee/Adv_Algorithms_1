import gc
import os
from dataclasses import dataclass
from time import perf_counter_ns
from typing import Callable, Dict, List, Optional

from graph import Graph, graph_from_file


@dataclass
class Analysis:
    size: int
    time: float

    def __init__(self, size: int, time: float):
        self.size = size
        self.time = time

    def __lt__(self, other):
        return self.size < self.size


MSTAlgorithm = Callable[[Graph], Graph]
ComplexityFunction = Callable[[int], float]


def run_algorithm(graph: Graph, algorithm: MSTAlgorithm, num_calls: int) -> float:
    gc.disable()
    start_time = perf_counter_ns()

    for _ in range(num_calls):
        algorithm(graph)

    end_time = perf_counter_ns()
    gc.enable()
    return (end_time - start_time) / num_calls


def measure_run_times(algorithm: MSTAlgorithm, num_calls: int) -> List[Analysis]:
    data: Dict[int, List[float]] = {}

    files: List[str] = os.listdir("dataset")

    for file in files:
        print("init " + file)
        graph: Graph = graph_from_file("dataset/" + file)
        estimate_time = run_algorithm(graph, algorithm, num_calls)

        size: int = graph.n

        if size not in data:
            data[size] = []

        data[size].append(estimate_time)

    avg_results: Dict[int, float] = {}
    for key, item in data.items():
        avg_results[key] = sum(item) / len(item)

    analysis: List[Analysis] = []

    for key, value in avg_results.items():
        analysis.append(Analysis(key, value))

    analysis.sort(key=lambda i: i.size)
    print(analysis)
    return analysis


def run_analysis(algorithm: MSTAlgorithm, complexity_function: ComplexityFunction,
                 num_calls: int = 1):
    analysis: List[Analysis] = measure_run_times(algorithm, num_calls)

    ratios: List[Optional[float]] = [0.0] + \
                                    [round(analysis[i + 1].time / analysis[i].time, 3) for i in
                                     range(len(analysis) - 1)]
    c_estimates = [round(analysis[i].time / complexity_function(analysis[i].size), 3)
                   for i in range(len(analysis))]
    print("Size\tTime(ns)\t\t\t\tCostant\t\t\t\t\tRatio")
    print(50 * "-")
    for index, item in enumerate(analysis):
        print(item.size, round(item.time, 2), '',
              c_estimates[index], '', ratios[index], sep="\t\t")

    print(50 * "-")
