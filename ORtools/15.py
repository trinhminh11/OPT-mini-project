from ortools.linear_solver import pywraplp


# Class Pacakge represent a Package, contain ID, capacity and cost
class Package:
	def __init__(self, ID, capacity, cost):
		self.ID = ID
		self.capacity = capacity
		self.cost = cost
	

# class Truck represent a Truck, contain ID, lower bound, upper bound, current capacity and current cost of that truck
class Truck:
	def __init__(self, ID, lower_bound, upper_bound):
		self.ID = ID
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound
	
		
# improt data
def import_data():
	packages = []
	trucks = []

	N, K = map(int, input().split())

	for i in range(N):
		l, c = map(float, input().split())
		packages.append(Package(i, l, c))
	
	for i in range(K):
		c1, c2 = map(float, input().split())
		trucks.append(Truck(i, c1, c2))
	
	return packages, trucks


class Solver:
	def __init__(self, packages, trucks):
		self.N = len(packages)
		self.K = len(trucks)

		self.packages = packages
		self.trucks = trucks

	def solve(self):
		solver: pywraplp.Solver = pywraplp.Solver.CreateSolver('CP_SAT')
		x = [[_ for _ in range(self.K)] for _ in range(self.N)]

		# create solver val, x[i][j] = 1 if there're a connection between node i and node j, 0 otherwise
		for i in range(self.N):
			for j in range(self.K):
				x[i][j] = solver.IntVar(0, 1,' ')

		# X transpose
		x_T = [[x[i][j] for i in range(self.N)] for j in range(self.K)]

		# 1 package can only assign to 1 truck
		for i in range(self.N):
			solver.Add(sum(x[i]) <= 1)

		# lower, upper bound contraint
		for i in range(self.K):
			solver.Add(sum( [x_T[i][j] * self.packages[j].capacity for j in range(self.N)] ) <= self.trucks[i].upper_bound)
			solver.Add(self.trucks[i].lower_bound <= sum( [x_T[i][j] * self.packages[j].capacity for j in range(self.N)] ))

		# objective function

		M = sum([sum([x_T[i][j] * self.packages[j].cost for j in range(self.N)]) for i in range(self.K)])

		solver.Maximize(M)

		# solve
		solver.Solve()

		self.result = []

		for i in range(self.N):
			self.result.append([])
			for j in range(self.K):
				self.result[i].append(int(x[i][j].solution_value()))
	
	def print_sol(self):
		print(sum([sum(self.result[i]) for i in range(self.N)]))

		for i, row in enumerate(self.result):
			try:
				print(i+1, row.index(1)+1)
			except:
				pass
				

def main():
	packages, trucks = import_data()

	sol = Solver(packages, trucks)

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()