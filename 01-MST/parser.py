from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Content:
    """
    A class for represent the content of a file after it is parsed.
    This class is designed for file produced by the stanford-algs' TestCaseGenerator.
    ...

    Attributes
    ----------
    n: int
        number of nodes inside the graph described in the file
    m: int
        number of edges inside the graph described in the file
    list_triple: List[Tuple[int, ...]]
        list of triple represented the edge that has as origin node as first element,
        target node as second element and weight the third element.
    """
    n: int
    m: int
    list_triple: List[Tuple[int, ...]]

    def __init__(self, n: int = 0, m: int = 0, list_triple: List[Tuple[int, ...]] = None):
        self.n: int = n
        self.m: int = m
        if list_triple is None:
            self.list_triple = []
        else:
            self.list_triple: List[Tuple[int, ...]] = list_triple


def parse(path: str) -> Content:
    """
    Parse the content of a file representing a graph

    Parameters
    ----------
    path : str
        the relative or absolute path to the input source file

    Returns
    -------
    content
        a object of type Content representing the content of the parsed file
    """
    content = Content()
    with open(path, "r", encoding="utf-8") as file:
        first_line: str = file.readline()
        # The fist line contains the "n" and "m" value, so it has to be splitted
        content.n = int(first_line.split()[0])
        content.m = int(first_line.split()[1])

        # Continuing to analyze the file
        for line in file.readlines():
            data: List[str] = line.split()
            # Creating a triple on the fly
            _triple: Tuple[int, ...] = int(data[0]), int(data[1]), int(data[2])
            # Adding the triple at the list inside the Content object
            content.list_triple.append(_triple)

    return content
