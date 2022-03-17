import gc, os
from time import perf_counter_ns
from typing import Callable, Dict, List

from graph import Graph, graph_from_file

MSTAlgorithm = Callable[[Graph], int]


def run_algorithm(graph: Graph, algorithm: MSTAlgorithm, num_calls: int) -> float:
    gc.disable()
    start_time = perf_counter_ns()

    for _ in range(num_calls):
        algorithm(graph)

    end_time = perf_counter_ns()
    gc.enable()
    return (end_time - start_time) / num_calls


def measure_run_times(algorithm: MSTAlgorithm, num_calls: int = 10000) \
        -> Dict[int, float]:

    results: Dict[int, List[float]] = {}

    files: List[str] = os.listdir("dataset")

    for file in files:
        graph: Graph = graph_from_file(file)
        estimate_time = run_algorithm(graph, algorithm, num_calls)
        
        size: int = graph.m  # m = |E|

        if not(size in results):
            results[size] = []

        results[size].append(estimate_time)

    avg_results: Dict[int, float] = {}

    for key in results.keys():
        avg_results[key] = sum(results[key])/len(results[key])

    return avg_results
