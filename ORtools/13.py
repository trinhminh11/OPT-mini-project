from ortools.sat.python import cp_model
# import data
def import_data():

	N, M = map(int, input().split())

	d = list(map(int, input().split()))
	
	c = list(map(int, input().split()))

	K = int(input())
	pairs = []

	for _ in range(K):
		i, j = map(int, input().split())

		pairs.append([i, j])
	
	return N, M, d, c, pairs

class Solver:
	def __init__(self, N, M, d, c, pairs):
		self.N = N
		self.M = M
		self.d = d
		self.c = c
		self.pairs = pairs

		# N * M
		self.X = [[0 for _ in range(self.M)] for _ in range(self.N)]
		self.Y = [0 for _ in range(self.N)]

	def solve(self):
		model = cp_model.CpModel()

		for i in range(self.N):
			for j in range(self.M):
				self.X[i][j] = model.NewIntVar(0, 1, f'x{i}{j}')

				if self.d[i] > self.c[j]:
					model.Add(self.X[i][j] == 0)
			
			model.Add(sum(self.X[i]) == 1)

			self.Y[i] = model.NewIntVar(1, self.N, f'y{i}')
		
		for pair in self.pairs:
			model.Add(self.Y[pair[0]-1] != self.Y[pair[1]-1])
		
		for i1 in range(self.N-1):
			for i2 in range(i1+1, self.N):	
				for j in range(self.M):
					b = model.NewBoolVar('b')

					model.Add(self.X[i1][j] + self.X[i2][j] == 2).OnlyEnforceIf(b)
					model.Add(self.X[i1][j] + self.X[i2][j] != 2).OnlyEnforceIf(b.Not())

					model.Add(self.Y[i1] != self.Y[i2]).OnlyEnforceIf(b)

		obj = model.NewIntVar(1, self.N, 'obj')

		model.AddMaxEquality(obj, self.Y)

		model.Minimize(obj)

		solver = cp_model.CpSolver()
		solver.Solve(model)

		self.result = []

		for i in range(self.N):
			for j in range(self.M):
				if solver.Value(self.X[i][j]) == 1:
					self.result.append([i+1, solver.Value(self.Y[i]), j+1])
		
	def print_sol(self):
		for result in self.result:
			print(*result)

def main():

	sol = Solver(*import_data())
	
	sol.solve()

	sol.print_sol()

if __name__ == "__main__":
	main()
