import math
import random

import evaluator
from approx_metric_tsp import approx_metric_tsp
from cheapest_insertion import cheapest_insertion
from random_insertion import random_insertion

def two_approx_function(n: int):
    return 2

def logn_function(n: int):
    return math.log2(n)

def main():
    random.seed(404)
    random_evaluation = evaluator.evaluate(random_insertion, logn_function)

    #evaluator.random_best_evaluation(1, random_evaluation)

    cheapest_evaluation = evaluator.evaluate(cheapest_insertion, two_approx_function)
    two_approx_evaluation = evaluator.evaluate(approx_metric_tsp, two_approx_function)

    evaluator.make_plots(random_evaluation, cheapest_evaluation, two_approx_evaluation)


if __name__ == '__main__':
    main()
