from sys import argv

from algorithms.kruskal_union_find import kruskal_union_find
from algorithms.naive_kruskal import naive_kruskal
from analyzer import run_analysis, print_results, mlogn, mn, compare_plot
from algorithms.prim import prim


def main():
    if len(argv) == 2 and argv[1] == "-r":
        print_results()
    else:

        num_calls = 100000
        print("Prim")
        prim_analysis = run_analysis(prim, mlogn, "Prim", num_calls)

        print("Kruskal union find")
        kruskal_union_find_analysis = run_analysis(kruskal_union_find, mlogn, "Kruskal_union_find", num_calls)

        print("Kruskal naive")
        naive_kruskal_analysis = run_analysis(naive_kruskal, mn, "Kruskal_naive", num_calls, True)

        compare_plot(prim_analysis, kruskal_union_find_analysis, naive_kruskal_analysis)


if __name__ == '__main__':
    main()
