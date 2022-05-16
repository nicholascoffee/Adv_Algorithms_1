from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Content:
    """
    Dataclass for represent content to insert in a graph

    Attributes
    ----------
    name: str
        the name of the graph for more readable reference for optimal solution
    n: int
        the total number of nodes in the graph
    weight_type: str
        the type of representation of the nodes. Useful to know how to calculate distance between nodes
    triples: List[Tuple[int, float, float]]
        list of triples for represent nodes and their coordinates
    """
    name: str
    n: int
    weight_type: str
    triples: List[Tuple[int, float, float]]

    def __init__(self, name: str = "", n: int = 0, weight_type: str = "",
                 triples: List[Tuple[int, float, float]] = None):
        self.name = name
        self.n = n
        self.weight_type = weight_type
        self.triples = [] if (triples is None) else triples


def parse(path: str) -> Content:
    with open(path, "r", encoding="utf-8") as file:
        # Create empty content
        content: Content = Content()
        # Read first line of file
        line: str = file.readline()

        # Iterate all the fileds until it finds where are the nodes
        while not line.startswith("NODE_COORD_SECTION"):
            if line.startswith("NAME:"):
                content.name = line.split()[1]
            elif line.startswith("DIMENSION:"):
                content.n = int(line.split()[1])
            elif line.startswith("EDGE_WEIGHT_TYPE"):
                content.weight_type = line.split()[1]
            # Read next line in any case
            line = file.readline()

        for line in file.readlines():
            # Remove initial and ending space
            line = line.strip()
            # Avoid "EOF" and empty lines
            if not line.startswith("EOF") and not line == "":
                data: List[str] = line.split()
                # Creating a triple on the fly
                trp: Tuple[int, float, float] = int(data[0]), float(data[1]), float(data[2])
                # Adding the triple at the list inside the Content object
                content.triples.append(trp)
    # Close the file
    file.close()
    return content
