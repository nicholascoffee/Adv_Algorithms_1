from graph import Graph

def sorted_edges(graph: Graph) -> list:
    edges = Graph.get_all_edges
    edges.sort()
    return edges

# A recursive function that uses visited[] and parent to detect cycle in subgraph reachable from vertex v

def isCyclicUtil(self,v,visited,parent):
 
    # Mark the current node as visited
    visited[v]= True
 
    # Recur for all the vertices adjacent to this vertex
    for i in self.graph[v]: 
        # If the node is not visited then recurse on it
        if  visited[i]==False :
            
            if(self.isCyclicUtil(i,visited,v)):
            
                return True
        
        # If an adjacent vertex is visited and not parent of current vertex, then there is a cycle
        elif  parent!=i:
            
            return True     

    return False
# Returns true if the graph contains a cycle, else false.

def isCyclic(self):
       
    # Mark all the vertices as not visited
    visited = [False] * (self.V)
     
    # Call the recursive helper function to detect cycle in different DFS trees
    
    for i in range(self.V):
           
        # Don't recur for u if it is already visited
        
        if visited[i] ==False:

            if(self.isCyclicUtil(i,visited,-1)) == True:
            
            return True
         
    return False


def naive_kruskal(graph: Graph) -> Graph:

    #empty graph to return with the solution
    
    A: graph = Graph(0)
    i=0
    #sorting the edges in crescent order

    edges = sorted_edges(Graph)
    
    #check for all the edges sorted the nodes
    for e in edges

        B: graph = A
        a = edges[i].__getattribute__(a)
        b = edges[i].__getattribute__(b)
        weight = edges[i].__getattribute__(weight)

    #add in the new graph if the graph created is still acyclic, else continue with the next ndoes
        
        if (B.add_edge(a,b,weight).isCyclic)
            A.add_edge(a,b,weight)
            
        i=i+1
    return A