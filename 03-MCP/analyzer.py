import gc
from sys import maxsize
from os import listdir
from time import perf_counter_ns
from math import log2
from typing import Callable, List
from dataclasses import dataclass, field
from graph import Graph, graph_from_file
from algorithms.karger_stein import recursive_contract

DATASET: List[str] = sorted(listdir("dataset"))

# Type alias
Time = float # Union[int, float]
MinimunCutAlgorithm = Callable[[Graph], int]

@dataclass
class Analysis:
    graph_name: str
    minimun_cost: int = field(default=maxsize) 
    execution_time: int = field(default=maxsize)
    # Useful for Karger & Stein's analisys
    discovery_time: int = field(default=maxsize, init=False)

def measure_wagner_stoer_algorithm(name: str, g: Graph) -> Analysis:
    """

    Parameters:
    -----------
    g: Graph
        is the graph where to executes the algorithm.

    Returns:
    --------
    Analysis
    """
    result: Analysis = Analysis(name)
    gc.disable()
    # Start first timer
    start_execution_timer: int = perf_counter_ns()
    for _ in range(int(log2(g.n)) ** 2):
        # Execute the Karger & Stein's algorithm
        min_cut: int = 0 # call the algorithm
        # Check if the new minimun cost is less than its previous
        if min_cut < result.minimun_cost:
            result.minimun_cost = min_cut
    # End first timer
    end_execution_timer: int = perf_counter_ns()
    gc.enable()
    # Elaborate total execution time
    result.execution_time = end_execution_timer - start_execution_timer
    return result

def measure_karger_stein_algorithm(name: str, g: Graph) -> Analysis:
    """
    Given a graph, the function executes log^2(n) the recursive_contract in order to have the error 
    probability less or equal 1/n.
    It returns the complete analysis of that istance problem with the discovery time.

    Parameters:
    -----------
    g: Graph
        is the graph where to executes the Karger & Stein's algorithms.

    Returns:
    --------
    Analysis
        the minimun cost, the execution time and the discovery time of that specific graph.
    """
    result: Analysis = Analysis(name)
    # Start first timer
    start_execution_timer: int = perf_counter_ns()
    for _ in range(int(log2(g.n)) ** 2):
        # Start second timer
        start_discovery_timer: int = perf_counter_ns()
        gc.disable()
        # Execute the Karger & Stein's algorithm
        min_cut: int = recursive_contract(g)
        gc.enable()
        # end second timer
        end_discovery_timer: int = perf_counter_ns()
        # Check if the new minimun cost is less than its previous
        if min_cut < result.minimun_cost:
            result.minimun_cost = min_cut
            result.discovery_time = end_discovery_timer - start_discovery_timer
    # End first timer
    end_execution_timer: int = perf_counter_ns()
    # Elaborate total execution time
    result.execution_time = end_execution_timer - start_execution_timer
    # TODO: Debug
    assert result.discovery_time <= result.execution_time
    return result

def test() -> None:
    for file_name in DATASET:
        path: str = f"./dataset/{file_name}"
        g: Graph = graph_from_file(path)
        # measure_alg(graph, algorithm, num_call)
        print(measure_karger_stein_algorithm(file_name, g))