import math
from typing import Tuple

from analyzer import run_analysis, measure_time
from algorithms.kruskal_union_find import kruskal_union_find
from algorithms.naive_kruskal import naive_kruskal
from algorithms.prim import prim

def mlogn(size: Tuple[int, int]) -> float:
    return size[1] * math.log2(size[0])

def mn(size: Tuple[int, int]) -> float:
    return size[1] * size[0]


def main():
    run_analysis(prim, mlogn, 10)
    #run_analysis(kruskal_union_find, mlogn, 10)
    #heap = Heap()

if __name__ == '__main__':
    main()
