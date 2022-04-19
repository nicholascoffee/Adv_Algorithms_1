import math
from typing import Tuple

from analyzer import run_analysis, Analysis
from prim import prim


def mlogn(size: int) -> float:
    return math.log2(size)


def main():
    run_analysis(prim, mlogn, 10)


if __name__ == '__main__':
    main()
