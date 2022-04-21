import math
from typing import Tuple

from analyzer import run_analysis, Analysis
from kruskal_union_find import kruskal_union_find
from naive_kruskal import naive_kruskal
from prim import prim


def mlogn(size: Tuple[int, int]) -> float:
    return size[1] * math.log2(size[0])


def main():
    run_analysis(prim, mlogn, 10)


if __name__ == '__main__':
    main()
