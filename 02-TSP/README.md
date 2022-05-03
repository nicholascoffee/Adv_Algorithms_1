# Second Assignment: Traveling Salesman Problem

## General Description
In this assignment you are asked to solve an intractable problem and to compare the execution times and the quality of the solutions that can be obtained with different approximation algorithms.
The problem to be analyzed is the "Traveling Salesman Problem" (TSP), defined as follows: given the coordinates x,y ofN points in the plane (the vertices), and a weight function w(u,v) defined for all pairs of points (the arcs), find the simple loop of minimum weight that visits all the N points. The weight function w(u,v) is defined as the Euclidean or Geographic distance between the points u and v (you can find details on how to calculate the distance in the dataset description) . The weight function is symmetric and respects the triangular inequality.

## Algorithms
The algorithms to implement are from two categories: (1) constructive heuristics; and (2) 2-approximate algorithm. 

* Constructive heuristics: choose two of the following constructive heuristics and implement them: Nearest Neighbor, Closest Insertion, Farthest Insertion, Random Insertion, Cheapest Insertion.

* 2-approximate algorithm: Implement the 2-approximate algorithm based on the minimum spanning tree.

## Dataset
The dataset contains 13 graphs, some from real test cases and some randomly generated. It is a subset of the dataset from TSPLIB and is in the file tsp_dataset.zip.

The first lines of each file contain some information about the instance, such as the number of N points (ranging from 14 to 1000) and the type of coordinates: Euclidean (EUC_2D) or Geographic (GEO). As an example the first lines of eil51.tsp are as follows:
```
NAME : eil51

COMMENT : 51-city problem (Christofides/Eilon)
TYPE : TSP
DIMENSION : 51
EDGE_WEIGHT_TYPE : EUC_2D
NODE_COORD_SECTION
1 37 52
2 49 49
3 52 64
4 20 26
...
```
The lines after NODE_COORD_SECTION contain the vertices of the graph: each line includes a vertex ID (unique integer) followed by the x and y coordinates which. The three values are separated by spaces. 

The following table summarizes some statistics of the dataset:

```
File	Description	N	Optimal solution
burma14.tsp	 Burma (Myanmar)	 14	3323
ulysses16.tsp	 Mediterranean Sea	 16	 6859
ulysses22.tsp	 Mediterranean Sea	 22	7013
eil51.tsp	Synthetic	51	426
berlin52.tsp	 Germany	52 	 7542
kroD100.tsp	Random	100	21294
kroA100.tsp	Random 	 100	21282
ch150.tsp	 Random	 150	 6528
gr202.tsp	 Europe	 202	 40160
gr229.tsp	Asia/Australia	229	134602
pcb442.tsp	 Drilling		442 	50778 
d493.tsp	Drilling	493	35002
dsj1000.tsp	Random	1000 	18659688 
```

## Input handling and distance computation
* GEO format: the x coordinate is the latitude, the y coordinate is the longitude
    * convert x, y coordinates to radians using the code specified in the TSPLIB FAQ (Q: I get wrong distances for problems of type GEO.). The formula uses the integer part of x and y (DOES NOT ROUND TO THE NEAREST INTEGER).
    
    * compute the geographic distance between points i and j using the FAQ code for "dij". The code uses the integer part of the distances (does not round).

* EUC_2D format: No coordinate conversions are needed in this case. Calculate the Euclidean distance and round the value to the nearest integer.

## Question 1
Run the three algorithms (the two constructive heuristics and 2-approximate) on the 13 graphs of the dataset. Show your results in a table like the one below (see the real assignment on Moodle). The rows in the table correspond to the problem instances. The columns show, for each algorithm, the weight of the approximate solution, the execution time and the relative error calculated as
ApproximateSolution−OptimalSolutionOptimalSolution

## Question 2
Comment on the results you have obtained: how do the algorithms behave with respect to the various instances? Is there an algorithm that always manages to do better than the others with respect to the approximation error? Which of the three algorithms you have implemented is more efficient?