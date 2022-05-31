# import from other files
import txtreader as tr
import Graph as gr

#import library needed
import networkx as nx
from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import os

class GUIdijkstra(Tk):
    def __init__(self):
        super().__init__()
        self.title("Dijkstra - 13520136")
        self.geometry("1000x1000")

        self.primary_color = "#E8F9FD"
        self.secondary_color = "#79DAE8"

        self.configure(bg=self.primary_color)

        self.pathname = ""
        self.SourceNode = ""
        self.SourceNodeIndex = -1
        self.DestNode = ""
        self.DestNodeIndex = -1
        self.isFirstClick = True

        self.fig, ax = plt.subplots()

        self.canvas = FigureCanvasTkAgg(self.fig,
                                    master = self) 

        self.browse_button = Button(master = self,
                    command = self.browse,
                    text = "Browse",
                    bg = self.secondary_color)

        self.browse_button.pack(pady=20)

        self.browse_label = Label(master = self,
                    text = "No File Selected",
                    bg = self.primary_color)

        self.browse_label.pack()

        self.plot_button = Button(master = self, 
                     command = self.plot,
                     text = "Plot",
                     state= "disable",
                    bg = self.secondary_color)

        self.plot_button.pack(pady=20)

        self.frame = Frame(master = self, bg = self.primary_color)

    def browse(self):
        currdir = os.getcwd()
        tempdir = filedialog.askopenfilenames(parent=self, initialdir=currdir, title='Please select a directory', filetypes = (('txt files','*.txt'),))

        self.pathname = "%s" % tempdir
        self.browse_label["text"] = self.pathname
        self.plot_button["state"] = "normal"

    def plot(self):

        def hilighter(event):
            (x,y)   = (event.xdata, event.ydata)
            counter = 0

            for key, value in self.pos.items():
                distance = pow(x-value[0],2)+pow(y-value[1],2)
                if distance < 0.005:
                    if self.isFirstClick:
                        self.SourceNode = key
                        if self.SourceNodeIndex == -1:
                            self.SourceNodeIndex = counter
                            self.colormap[self.SourceNodeIndex] = "r"
                        else:
                            self.colormap[self.SourceNodeIndex] = "b"
                            self.SourceNodeIndex = counter
                            self.colormap[self.SourceNodeIndex] = "r"
                    else:
                        self.DestNode = key
                        if self.DestNodeIndex == -1:
                            self.DestNodeIndex = counter
                            self.colormap[self.DestNodeIndex] = "y"
                        else:
                            self.colormap[self.DestNodeIndex] = "b"
                            self.DestNodeIndex = counter
                            self.colormap[self.DestNodeIndex] = "y"
                    self.isFirstClick = not self.isFirstClick
                    drawgraph()
                counter += 1

        def reset():
            for i in range(len(self.colormap)):
                self.colormap[i] = "b"
            
            for widget in self.frame.winfo_children():
                widget.destroy()

            self.SourceNodeIndex = -1
            self.DestNodeIndex = -1
            self.isFirstClick = True

            self.dijkstra_button = Button(master = self.frame, 
                     command = dijkstra,
                     text = "Dijkstra",
                    bg = self.secondary_color)

            self.dijkstra_button.pack()

            drawgraph()
            

        def dijkstra():
            if self.DestNodeIndex != -1:
                for widget in self.frame.winfo_children():
                    widget.destroy()

                self.g.dijkstra(self.SourceNodeIndex)
                self.g.updatePathRec(self.DestNodeIndex)
                pathDijkstra = self.g.path.split()
                self.now = 0

                self.reset_button = Button(master = self.frame, 
                     command = reset,
                     text = "Reset",
                    bg = self.secondary_color)

                self.reset_button.pack()

                def nextGraph():
                    if self.now < len(pathDijkstra)-2:
                        self.now += 1
                        counter = 0 
                        for node in self.G:
                            if node == pathDijkstra[self.now]:
                                self.colormap[counter] = "orange"
                                break
                            counter += 1
                        drawgraph()

                def prevGraph():
                    if self.now > 0:
                        counter = 0 
                        for node in self.G:
                            if node == pathDijkstra[self.now]:
                                self.colormap[counter] = "b"
                                break
                            counter += 1
                        self.now -= 1
                        drawgraph()

                self.next_button = Button(master = self.frame, 
                        command = nextGraph,
                        text = "Next",
                        bg = self.secondary_color)

                self.next_button.pack()

                self.prev_button = Button(master = self.frame, 
                        command = prevGraph,
                        text = "Prev",
                        bg = self.secondary_color)

                self.prev_button.pack()

                text = "Distance from source = " + str(self.g.dist[self.DestNodeIndex]) + "  Path: " + self.g.path 
                info = Label(master = self.frame, text = text, bg = self.primary_color)
                info.pack(pady = 20)

                drawgraph()
        

        def drawgraph():
            self.fig.clear() 
            nx.draw_networkx_nodes(self.G, self.pos, node_color=self.colormap, node_size = 500)
            nx.draw_networkx_edges(self.G, self.pos, edgelist = self.G.edges() , edge_color='black')
            nx.draw_networkx_labels(self.G, self.pos)
            edge_labels = nx.get_edge_attributes(self.G, "weight")

            array = []
            for key in edge_labels:
                array.append(key)
                swaptuple = (key[1], key[0])
                if swaptuple in array:
                    edge_labels[key] = str(edge_labels[swaptuple]) + '/' + str(edge_labels[key])

            nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels)

            self.canvas.draw()
            self.cnt = self.canvas.mpl_connect('button_press_event', hilighter)
            self.canvas.get_tk_widget().pack()

        for widget in self.frame.winfo_children():
            widget.destroy()
        
        try:
            self.canvas.mpl_disconnect(self.cnt)
        except:
            pass
                    
        reader = tr.txtreader(self.pathname)
        NodeName, AdjacencyMatrix =  reader.toStructuredForms()
        self.g   = gr.Graph(NodeName, AdjacencyMatrix)
        self.G, self.pos = self.g.getnxGraph()
        
        self.colormap=[]
        for node in self.G:
            self.colormap.append("b")

        self.SourceNodeIndex = -1
        self.DestNodeIndex = -1
        self.isFirstClick = True

        self.dijkstra_button = Button(master = self.frame, 
                     command = dijkstra,
                     text = "Dijkstra",
                    bg = self.secondary_color)

        self.dijkstra_button.pack()
        
        self.frame.pack()
        drawgraph()


if __name__ == "__main__":
    app = GUIdijkstra()
    app.mainloop()