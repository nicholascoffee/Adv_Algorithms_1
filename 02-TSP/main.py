import math
import random
import sys
import time

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

    # execute the multiple random study with:
    # python3 main.py --multiple-random
    if "--multiple-random" in sys.argv:
        print("PERFORMING MULTIPLE RANDOM STUDY OVER 500 INSTANCES")
        print("_"*20)
        print()
        random_evaluation = evaluator.evaluate(random_insertion, 1)
        evaluator.random_best_evaluation(1000, random_evaluation)
        return

    random_evaluation = evaluator.evaluate(random_insertion)
    evaluator.pretty_print(random_evaluation, logn_function, "random")

    cheapest_evaluation = evaluator.evaluate(cheapest_insertion)
    evaluator.pretty_print(cheapest_evaluation, two_approx_function, "cheapest")

    two_approx_evaluation = evaluator.evaluate(approx_metric_tsp)
    evaluator.pretty_print(two_approx_evaluation, two_approx_function, "2_approx")

    evaluator.make_plots(random_evaluation, cheapest_evaluation, two_approx_evaluation)


if __name__ == '__main__':
    main()
