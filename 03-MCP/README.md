# Third Assignment: Minimun Cut Problem
In this assigment your are asked to compare the performance of two algorithms for the min-cut problem for weighted graphs:

* Stoer and Wagner's deterministic algorithm 
* Karger and Stein's randomized algorithm

## Dataset
The dataset contains 56 graphs, ranging in size from 10 to 500 vertices, generated randomly with [stanford-algs' TestCaseGenerator](https://github.com/beaunus/stanford-algs/tree/master/testCases/course3/assignment1SchedulingAndMST/question3).
Each file describes an undirected graph with positive integer weights using the following format:

[number_of_nodes] [number_of_edges]

[one_node_edge_1] [other_node_edge_1] [weight_edge_1]  
[one_node_edge_2] [other_node_edge_2] [weight_edge_2]  
[one_node_edge_3] [other_node_edge_3] [weight_edge_3]  

For example, a row "2 3 8874" indicates that there is an edge connecting vertex 2 to vertex 3 with weight 8874. Weights are positive but not necessarily distinct.

## Question 1
Run the two algorithms you have implemented on the graphs of the dataset. For the Karger e Stein algorithm, use a number of repetitions that guarantees a probability to obtain a global min-cut fo at least 1−1/n.

Measure the execution times of the algorithms and create a graph showing the increase of execution times as the number of vertices in the graph increases. Compare the measured times with the asymptotic complexity of the algorithms. For each problem instance, report the weight of the minimum cut obtained by your code.

You can use a timeout to limit the execution time of large instances if it became too large.

## Question 2
Measure the discovery time of the Karger and Stein algorithm. The discovery time is the instant (in seconds) when the algorithm finds the minimum cost cut. Compare the discovery time with the overall execution time for each of the graphs in the dataset.

## Question 3
Comment on the results you have obtained: how do the algorithms behave with respect to the various instances? There is an algorithm that is always better than the other? Which algorithm is more efficient? 