# Union Find with union-by-size.
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class UnionFindNode(int):
	"""
    A dataclass to represent a single node in the parent graph.

    Attributes
    ----------
    data : int
        the unique value associate to the node
    parent : UnionFindNode = slef
        the parent of the node
    size : int = 1
        number of nodes that are underlying of the specific node
    """
	data: int
	parent: 'UnionFindNode' = field(init=False)
	size: int = 1

	def __post_init__(self):
		'''Function to defear the initialization of the parent node'''
		self.parent = self

class UnionFindSet():
	"""
    A class to represent sets of node in the union-find.

    Attributes
    ----------
    _map : Dict[int, UnionFindNode]
        a key-value store for the sets of nodes 

    Methods
    -------
    def make(self, data: int) -> None:
        create a key 'data' in the dict and the associate UnionFindNode as item
	def find(self, data: int) -> UnionFindNode:
		return the root parent of the node associate to that value
	def union(self, data1: int, data2: int) -> None:
		create a unique sets from the two nodes associate to the given values
    """
	_map: Dict[int, UnionFindNode] = {}
		
	def make(self, data: int) -> None:
		# create a new set with x as its member
		self._map[data] = UnionFindNode(data)

	def find(self, data: int) -> UnionFindNode:
		element: UnionFindNode = self._map[data]
		parent: UnionFindNode = element.parent
		if element != parent:
			element = element.parent
			parent = parent.parent
		return element

	def union(self, data1: int, data2: int) -> None:
		# getting the two roots of the sets
		root1: UnionFindNode = self.find(data1)
		root2: UnionFindNode = self.find(data2)
		if (root1 == root2): return
		elif (root1.size > root2.size):
			setattr(root2, 'parent', root1)
			setattr(root1, 'size', root1.size + root2.size)
		else:
			setattr(root1, 'parent', root2)
			setattr(root2, 'size', root2.size + root1.size)

	def toString(self) -> None:
		for key, item in self._map.items():
			print(f'Node: {key}, Parent {item}')
