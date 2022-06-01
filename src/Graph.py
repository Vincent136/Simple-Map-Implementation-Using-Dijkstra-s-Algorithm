import networkx as nx
import timeit
import sys

class Graph:

    def __init__(self, NodeNames, AdjacencyMatrix):
        self.NodeNames = NodeNames
        self.AdjacencyMatrix = AdjacencyMatrix
        self.row = len(self.AdjacencyMatrix)
        self.col = len(self.AdjacencyMatrix[0])
        self.path = ""

    #fungsi untuk mengembalikan layout graph menggunakan networkx
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

    #fungsi untuk menentukan jarak terpendek node yang terdapat pada queue
    def minDistance(self,queue):
        
        minimum = sys.maxsize
        min_index = -1 
        
        for i in range(len(self.dist)):
            if self.dist[i] < minimum and i in queue:
                minimum = self.dist[i]
                min_index = i

        return min_index

    #fungsi untuk mengupdate path yang dihasilkan
    def updatePathRec(self, j):
        if self.parent[j] == -1 :
            self.path += self.NodeNames[j] + " "
            return
        self.updatePathRec(self.parent[j])
        self.path += self.NodeNames[j] + " "
 
 
    #fungsi algoritma dijkstra
    def dijkstra(self, src):

        start = timeit.default_timer()

        self.dist = [sys.maxsize] * self.row
        self.parent = [-1] * self.row

        self.path = ""
     
        queue = []
        for i in range(self.row):
            queue.append(i)

        self.dist[src] = 0

        iteration_count = 0
        stage_count = 0
             
        while len(queue) != 0:

            u = self.minDistance(queue)
 
            queue.remove(u)
            
            for i in range(self.col):
                if self.AdjacencyMatrix[u][i] != 0 and i in queue:
                    
                    if self.dist[u] + self.AdjacencyMatrix[u][i] < self.dist[i]:
                        self.dist[i] = self.dist[u] + self.AdjacencyMatrix[u][i]
                        self.parent[i] = u
                    iteration_count += 1
            stage_count += 1

        
        stop = timeit.default_timer()
        return stage_count, iteration_count, (stop - start)*1000

    
    # Referensi Kode: https://www.geeksforgeeks.org/printing-paths-dijkstras-shortest-path-algorithm/