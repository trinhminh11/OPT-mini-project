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
def import_data():
	#list contains Nodes object, Nodes[0] represent starting location
	Nodes = [Node(0, 0, float('inf'), 0)]
	time_matrix = []

	#number of Node
	N = int(input())

	#get Node info
	for i in range(N):
		e, l, d = map(int, input().split())
		Nodes.append(Node(i+1, e, l, d))
	
	#get time matrix info
	for i in range(N+1):
		time_matrix.append(list(map(int, input().split())))

    # return Nodes and Time matrix
	return Nodes, time_matrix


class Truck:
	def __init__(self, time_matrix):
		self.solRoute = []    
		self.time_matrix = time_matrix

	def check_constraint(self, Route):
		current_time = Route[0].timeDone

		for i in range(len(Route)-1):
			current_time += self.time_matrix[Route[i].ID][Route[i+1].ID]
			
			# if we arrived before Time Window, we'll wait.
			if current_time < Route[i+1].e:
				current_time = Route[i+1].e + Route[i+1].d
				Route[i+1].timeDone = current_time

			#if we arrived inside the Time Window 
			elif Route[i+1].e <= current_time <= Route[i+1].l:
				current_time += Route[i+1].d
				Route[i+1].timeDone = current_time
			
			#if we arrived after Time Window
			else:
				return False
		
		return True
	

	# find best index to insert a node to route
	def Insert(self, node):
		temp_Route = self.solRoute.copy()
		best_Route = self.solRoute.copy()
		best_time = float('inf')

		for i in range(1, len(self.solRoute)+1):
			# early stopping	
			if node.e < temp_Route[i-1].timeDone:
				break

			# insert node to temp Route
			temp_Route.insert(i, node)

			# check if temp Route sastisfied Constraint
			if self.check_constraint(temp_Route):
				#if temp Route better than best Route, update best Route
				if temp_Route[-1].timeDone < best_time:
					best_time = temp_Route[-1].timeDone
					best_Route = temp_Route.copy()
			
			# reset temp Route
			temp_Route = self.solRoute.copy()
		
		# if we update best time, meaning that we have a better Route, update solution Route
		if best_time != float('inf'):
			self.solRoute = best_Route.copy()
			

class Solver:
	def __init__(self, Nodes, time_matrix):
		self.Nodes = Nodes[1:]
		self.time_matrix = time_matrix
		self.truck = Truck(time_matrix)
		self.truck.solRoute.append(Nodes[0])

	
	def solve(self):
		for node in self.Nodes:
			self.truck.Insert(node)
	
	def print_sol(self):
		print(len(self.truck.solRoute[1:]))

		for node in self.truck.solRoute[1:]:
			print(node.ID, end = " ")
	
	def export_sol(self, file):
		with open(file, 'w') as f:
			f.write(str(len(self.truck.solRoute[1:])))
			f.write("\n")

			for node in self.truck.solRoute[1:]:
				f.write(f'{node.ID} ')
	


def main():
	Nodes, time_matrix = import_data()

	sol = Solver(Nodes, time_matrix)

	sol.solve()

	sol.print_sol()

	# try:
	# 	sol.export_sol('12/output.txt')
	# except:
	# 	sol.export_sol('output.txt')


if __name__ == "__main__":
	main()