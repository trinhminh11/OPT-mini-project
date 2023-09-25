random_seed = 11042004

#Nodes object represent ID of Node, earliest and latest time to serve and time to delivery package
class Node:
	def __init__(self, ID, e, l, d):
		self.ID = ID
		self.e = e
		self.l = l
		self.d = d

		#time after delivery package
		self.timeDone = 0
	
	#printing for debug
	def __str__(self):
		return f'ID: {self.ID}, e: {self.e}, l: {self.l}, d: {self.d}, timeDone: {self.timeDone}.'
	
#import data from file
def import_data(file):
	#list contains Nodes object, Nodes[0] represent starting location
	Nodes: list[Node] = [Node(0, 0, 0, 0)]
	Time_matrix: list[list[int]] = []
	with open(file, 'r') as f:

		#number of Node
		N = int(f.readline())

		#get Node info
		for i in range(N):
			e, l, d = map(int, f.readline().split())
			Nodes.append(Node(i+1, e, l, d))
		
		#get time matrix info
		for i in range(N+1):
			Time_matrix.append(list(map(int, f.readline().split())))

	return Nodes, Time_matrix