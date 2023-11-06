from CONSTANT import Node, import_data


class Truck:
	def __init__(self, Time_matrix):
		self.solRoute: list[Node] = []    
		self.Time_matrix: list[list] = Time_matrix

	def check_constraint(self, Route: list[Node]):
		current_time = 0

		for i in range(len(Route)-1):
			current_time += self.Time_matrix[Route[i].ID][Route[i+1].ID]
			
			# if we arrived before Time Window, we'll wait.
			if current_time < Route[i+1].e:
				current_time = Route[i+1].e + Route[i+1].d

			#if we arrived inside the Time Window 
			elif Route[i+1].e <= current_time <= Route[i+1].l:
				current_time += Route[i+1].d

			#if we arrived after Time Window
			else:
				return False

			Route[i+1].timeDone = current_time

		
		return True
	


class Solver:
	def __init__(self, Nodes, Time_matrix):
		self.Nodes: list[Node] = Nodes
		self.n = len(self.Nodes) - 1
		self.Time_matrix: list[list] = Time_matrix
		self.truck = Truck(Time_matrix)
		self.truck.solRoute.append(Nodes[0])


	
	def solve(self):
		used = [False for _ in range(self.n)]
		permu = [i+1 for i in range(self.n)]

		self.best_Route = []

		def backtrack(pos):
			if pos == self.n:
				self.truck.solRoute = [self.Nodes[0]]
				for i in range(self.n):
					if self.truck.check_constraint(self.truck.solRoute + [self.Nodes[permu[i]]]):
						self.truck.solRoute.append(self.Nodes[permu[i]])


				if len(self.truck.solRoute) > len(self.best_Route):
					self.best_Route = self.truck.solRoute

				elif len(self.truck.solRoute) == len(self.best_Route):
					if self.truck.solRoute[-1].timeDone < self.best_Route[-1].timeDone:
						self.best_Route = self.truck.solRoute

				return

			for i in range(self.n):
				if not used[i]:
					permu[pos] = i+1
					used[i] = True
					backtrack(pos+1)
					used[i] = False

		backtrack(0)

		self.truck.solRoute = self.best_Route


	
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
	try:
		Nodes, Time_matrix = import_data('12/test.txt')
	except:
		Nodes, Time_matrix = import_data('test.txt')

	sol = Solver(Nodes, Time_matrix)

	sol.solve()

	sol.print_sol()

	try:
		sol.export_sol('12/output.txt')
	except:
		sol.export_sol('output.txt')


if __name__ == "__main__":
	main()