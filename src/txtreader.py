

class txtreader:
    def __init__(self, filename):
        self.Lines = []
        with open(filename) as fp:
            self.Lines = fp.readlines()

    def toStructuredForms(self):
        NodeName = []
        AdjacencyMatrix = []

        for line in self.Lines:
            AdjacencyArray=[]
            split = line.split()
            NodeName.append(split[0])
            for i in range(1,len(split)):
                AdjacencyArray.append(int(split[i]))
            AdjacencyMatrix.append(AdjacencyArray)

        return NodeName, AdjacencyMatrix            