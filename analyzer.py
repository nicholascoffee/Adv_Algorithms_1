import gc, os
from dataclasses import dataclass
from time import perf_counter_ns
from typing import Callable, Dict, List, Optional, Tuple

from graph import Graph, graph_from_file


@dataclass
class Analysis:
    size: int
    time: float

    def __init__(self, size: int, time: float):
        self.size = size
        self.time = time


MSTAlgorithm = Callable[[Graph], Graph]


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

    for file in files:
        graph: Graph = graph_from_file("dataset/" + file)
        estimate_time = run_algorithm(graph, algorithm, num_calls)

        size: Tuple[int, int] = (graph.n, graph.m)

        if not (size in data):
            data[size] = []

        data[size].append(estimate_time)

    avg_results: Dict[Tuple[int, int], float] = {}
    for key in data.keys():
        avg_results[key] = sum(data[key]) / len(data[key])

    sizes = list(avg_results.keys())
    sizes.sort() # TODO

    analysis: List[Analysis] = []

    for i in sizes:
        analysis.append(Analysis(i, avg_results[i])) # TODO

    return analysis


def run_analysis(algorithm: MSTAlgorithm, num_calls: int = 1000):
    analysis: List[Analysis] = measure_run_times(algorithm, num_calls)

    ratios: List[Optional[float]] = [0.0] + \
                                    [round(analysis[i + 1].time / analysis[i].time, 3) for i in
                                     range(len(analysis) - 1)]
    c_estimates = [round(analysis[i].time / analysis[i].size, 3) for i in range(len(analysis))]
