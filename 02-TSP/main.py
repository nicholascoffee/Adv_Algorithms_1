import evaluator
from approx_metric_tsp import approx_metric_tsp
from cheapest_insertion import cheapest_insertion
from random_insertion import random_insertion


def main():
    evaluator.evaluate(approx_metric_tsp)


if __name__ == '__main__':
    main()
