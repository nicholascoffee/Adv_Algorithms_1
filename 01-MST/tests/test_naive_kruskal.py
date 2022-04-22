import unittest
from time import perf_counter
from typing import TextIO
from unittest import TestCase

from parameterized import parameterized

import parser
from graph import Graph, graph_from_file
from naive_kruskal import naive_kruskal

tot_time = 0
tot_count = 0


class TestNaiveKruskal(TestCase):
    def __init__(self, a):
        super().__init__(a)

    @parameterized.expand(
        ['random_10_40.txt', 'random_11_40.txt', 'random_12_40.txt', 'random_13_80.txt', 'random_14_80.txt',
         'random_15_80.txt', 'random_16_80.txt', 'random_17_100.txt', 'random_18_100.txt', 'random_19_100.txt',
         'random_1_10.txt', 'random_20_100.txt', 'random_21_200.txt', 'random_22_200.txt', 'random_23_200.txt',
         'random_24_200.txt', 'random_25_400.txt', 'random_26_400.txt', 'random_27_400.txt', 'random_28_400.txt',
         'random_29_800.txt', 'random_2_10.txt', 'random_30_800.txt', 'random_31_800.txt', 'random_32_800.txt',
         'random_33_1000.txt', 'random_34_1000.txt', 'random_35_1000.txt', 'random_36_1000.txt', 'random_37_2000.txt',
         'random_38_2000.txt', 'random_39_2000.txt', 'random_3_10.txt', 'random_40_2000.txt', 'random_41_4000.txt',
         'random_42_4000.txt', 'random_43_4000.txt', 'random_44_4000.txt', 'random_45_8000.txt', 'random_46_8000.txt',
         'random_47_8000.txt', 'random_48_8000.txt', 'random_49_10000.txt', 'random_4_10.txt', 'random_50_10000.txt',
         'random_5_20.txt', 'random_6_20.txt', 'random_7_20.txt', 'random_8_20.txt', 'random_9_40.txt'])
    def test_naive_kruskal(self, file):
        global tot_time
        global tot_count

        print(tot_count)
        graph: Graph = graph_from_file("dataset/input_" + file)

        start = perf_counter()
        # ----------  algorithm call  ----------
        mst: Graph = naive_kruskal(graph)
        ########################################
        end = perf_counter()

        print(mst.edges)

        tot_time += (end - start)
        tot_count += 1

        print(tot_time / tot_count)

        result: int = mst.sum_weights()

        file: TextIO = open("dataset/output_" + file)
        th_result: int = int(file.readline())
        file.close()


        self.assertEqual(th_result, result)


if __name__ == '__main__':
    unittest.main()
