import math
from typing import Tuple

from algorithms.kruskal_union_find import kruskal_union_find
from algorithms.naive_kruskal import naive_kruskal
from analyzer import run_analysis
from algorithms.prim import prim


def mlogn(size: Tuple[int, int]) -> float:
    return size[1] * math.log2(size[0])


def mn(size: Tuple[int, int]) -> float:
    return size[1] * size[0]


def main():
    num_calls = 100000
    print("Prim")
    run_analysis(prim, mlogn, "Prim", num_calls)

    print("Kruskal union find")
    run_analysis(kruskal_union_find, mlogn, "Kruskal_union_find", num_calls)

    print("Kruskal naive")
    run_analysis(naive_kruskal, mn, "Kruskal_naive", num_calls)


if __name__ == '__main__':
    main()
