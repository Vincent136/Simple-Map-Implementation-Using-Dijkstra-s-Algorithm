import txtreader as tr
import Graph as gr
import networkx as nx
import matplotlib.pyplot as plt

reader = tr.txtreader("test.txt")
NodeName, AdjacencyMatrix =  reader.toStructuredForms()
g = gr.Graph(NodeName, AdjacencyMatrix)
G, pos = g.getnxGraph()


nx.draw_networkx_nodes(G, pos, node_size = 500)
nx.draw_networkx_edges(G, pos, edgelist = G.edges() , edge_color='black')
nx.draw_networkx_labels(G, pos)
edge_labels = nx.get_edge_attributes(G, "weight")

array = []
for key in edge_labels:
    array.append(key)
    swaptuple = (key[1], key[0])
    if swaptuple in array:
        edge_labels[key] = str(edge_labels[swaptuple]) + '/' + str(edge_labels[key])

nx.draw_networkx_edge_labels(G, pos, edge_labels)
plt.axis('off')
plt.show()