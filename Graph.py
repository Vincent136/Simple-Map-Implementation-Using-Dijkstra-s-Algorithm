import networkx as nx

class Graph:

    def __init__(self, NodeNames, AdjacencyMatrix):
        self.NodeNames = NodeNames
        self.AdjacencyMatrix = AdjacencyMatrix
        self.row = len(self.AdjacencyMatrix)
        self.col = len(self.AdjacencyMatrix[0])
        self.dist = [float("Inf")] * self.row
        self.parent = [-1] * self.row
        self.path = ""

    def getnxGraph(self):
        G = nx.DiGraph()

        weighted_array_tuple = []

        for i in range(self.row):
            for j in range(self.col):
                if(self.AdjacencyMatrix[i][j] != 0):
                    weighted_array_tuple.append((self.NodeNames[i], self.NodeNames[j], self.AdjacencyMatrix[i][j]))

        G.add_nodes_from(self.NodeNames)
        G.add_weighted_edges_from(weighted_array_tuple)
        pos = nx.spring_layout(G)

        return G, pos

    
    def minDistance(self,queue):
        
        minimum = float("Inf")
        min_index = -1
         
        
        for i in range(len(self.dist)):
            if self.dist[i] < minimum and i in queue:
                minimum = self.dist[i]
                min_index = i
        return min_index

 
    def updatePathRec(self, j):
        if self.parent[j] == -1 :
            self.path += self.NodeNames[j] + " "
            return
        self.updatePathRec(self.parent[j])
        self.path += self.NodeNames[j] + " "
 
 
    
    def dijkstra(self, src):

        self.dist = [float("Inf")] * self.row
        self.parent = [-1] * self.row

        self.path = ""
     
        queue = []
        for i in range(self.row):
            queue.append(i)

        self.dist[src] = 0
             
        while queue:

            u = self.minDistance(queue)
 
            queue.remove(u)
            
            for i in range(self.col):
                if self.AdjacencyMatrix[u][i] and i in queue:
                    if self.dist[u] + self.AdjacencyMatrix[u][i] < self.dist[i]:
                        self.dist[i] = self.dist[u] + self.AdjacencyMatrix[u][i]
                        self.parent[i] = u
    
    # Referensi Kode: https://www.geeksforgeeks.org/printing-paths-dijkstras-shortest-path-algorithm/