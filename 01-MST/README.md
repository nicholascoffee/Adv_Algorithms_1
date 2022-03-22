# First Assignment: Minimun Spanning Tree
In the first assignment you will compare three algorithms for the Minimum Spanning Tree problem:

* Prim's Algorithm implemented with a Heap

* Naive Kruskal's Algorithm with O(m*n) complexity

* Efficient Kruskal's Algorithm based on Union-Find

## Dataset
The dataset contains 68 example graphs, ranging in size from 10 to 100,000 vertices,  generated randomly [with stanford-algs' TestCaseGenerator](https://github.com/beaunus/stanford-algs/tree/master/testCases/course3/assignment1SchedulingAndMST/question3).

Each file describes an undirected graph with integer weights using the following format:

[number_of_nodes] [number_of_edges]

[one_node_edge_1] [other_node_edge_1] [weight_edge_1]  
[one_node_edge_2] [other_node_edge_2] [weight_edge_2]  
[one_node_edge_3] [other_node_edge_3] [weight_edge_3]   
...

For example, a row "2 3 -8874" indicates that there is an edge connecting vertex 2 to vertex 3 with weight -8874.

Weights should **NOT** be assumed to be positive nor distinct.

## Question 1

Run the three algorithms you have implemented (Prim, Kruskal naive and Kruskal efficient) on the graphs of the dataset.

Measure the execution times of the three algorithms and create a graph showing the increase of execution times as the number of vertices in the graph increases.

Compare the measured times with the asymptotic complexity of the algorithms.

For each problem instance, report the weight of the minimum spanning tree obtained by your code.

## Question 2

Comment on the results you have obtained: how do the algorithms behave with respect to the various instances? There is an algorithm that is always better than the others? Which of the three algorithms you have implemented is more efficient? 