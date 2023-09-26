from CONSTANT import Node, import_data


class Truck:
	def __init__(self, Time_matrix):
		self.solRoute: list[Node] = []    
		self.Time_matrix: list[list] = Time_matrix

	def check_constraint(self, Route: list[Node]):
		current_time = Route[0].timeDone

		for i in range(len(Route)-1):
			current_time += self.Time_matrix[Route[i].ID][Route[i+1].ID]
			
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
	def Insert(self, node: Node):
		temp_Route: list[Node] = self.solRoute.copy()
		best_Route: list[Node] = self.solRoute.copy()
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
	def __init__(self, Nodes, Time_matrix):
		self.Nodes: list[Node] = Nodes[1:]
		self.Time_matrix: list[list] = Time_matrix
		self.truck = Truck(Time_matrix)
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
	Nodes, Time_matrix = import_data('12/test.txt')

	sol = Solver(Nodes, Time_matrix)
	sol.solve()
	sol.print_sol()
	sol.export_sol('12/output.txt')


if __name__ == "__main__":
	main()