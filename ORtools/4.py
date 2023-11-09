from ortools.sat.python import cp_model

#import data
def import_data():
	distance_matrix = []
	cost_matrix = []
	N, M = map(int, input().split())

	for _ in range(N):
		cost_matrix.append(list(map(int, input().split())))


	for _ in range(M+1):
		distance_matrix.append(list(map(int, input().split())))
	
	Q = list(map(int, input().split()))
	
	
	return N, M, cost_matrix, distance_matrix, Q


class Solver:
	def __init__(self, N, M, cost_matrix, distance_matrix, Q):
		self.N = N
		self.M = M
		# M + 2 * N
		self.cost_matrix = [[0]*self.N ] + [[cost_matrix[i][j] for i in range(self.N)] for j in range(self.M)] + [[0]*self.N ]
		
		# for c in self.cost_matrix:
		# 	print(c)
		
		# print(Q)
		
		# M+1 * M+2
		self.distance_matrix = [distance_matrix[i] + [distance_matrix[i][0]] for i in range(M+1)]

		self.Q = Q

		# M+1 * M+2
		self.X = [[0 for _ in range(self.M+2)] for _ in range(self.M+1)]
	
	def solve(self):
		model = cp_model.CpModel()
		max_dist = sum([max(self.distance_matrix[i]) for i in range(self.M+1)])

		dist = [model.NewIntVar(0, max_dist, 'dist') for _ in range(self.M+2)]

		model.Add(dist[0] == 0)

		# current cost
		q = [_ for _ in range(self.N)]
		
		for i in range(self.M+1):
			for j in range(self.M+2):
				self.X[i][j] = model.NewIntVar(0, 1, f'x{i}{j}')
			
			model.Add(self.X[i][i] == 0)

			model.Add(sum(self.X[i]) <= 1)
		
		model.Add(self.X[0][-1] == 0)
		model.Add(sum(self.X[0]) == 1)
		model.Add(sum([self.X[i][0] for i in range(self.M+1)]) == 0)

		for j in range(1, self.M+1):
			model.Add(sum([self.X[i][j] for i in range(self.M+1)]) <= 1)

		model.Add(sum([self.X[i][-1] for i in range(self.M+1)]) <= 1)
		
		for i in range(self.M+1):
			for j in range(self.M+1):
				b = model.NewBoolVar('b')
				model.Add(self.X[i][j] == 1).OnlyEnforceIf(b)
				model.Add(self.X[i][j] == 0).OnlyEnforceIf(b.Not())
				model.Add(sum(self.X[j]) == 1).OnlyEnforceIf(b)

				model.Add(dist[j] == dist[i] + self.distance_matrix[i][j]).OnlyEnforceIf(b)
		
		for i in range(self.M+1):
			b = model.NewBoolVar('b')
			model.Add(self.X[i][-1] == 1).OnlyEnforceIf(b)
			model.Add(self.X[i][-1] != 1).OnlyEnforceIf(b.Not())
			model.Add(dist[-1] == dist[i] + self.distance_matrix[i][-1]).OnlyEnforceIf(b)
		
		for k in range(self.N):
			q[k] = sum([self.X[i][j] * self.cost_matrix[j][k] for i in range(self.M+1) for j in range(self.M+2)] )

			model.Add(q[k] >= self.Q[k])
		
		model.Minimize(dist[-1])

		solver = cp_model.CpSolver()

		solver.Solve(model)


		self.result = []

		current = 0

		while current != self.M+1:
			for j in range(self.M+2):
				if solver.Value(self.X[current][j]) == 1:
					self.result.append(j)
					current = j

		print(solver.Value(dist[-1]))
		print(solver.ObjectiveValue())

		for i in range(self.M+2):
			print(solver.Value(dist[i]), end = " ")
		print()

	def print_sol(self):
		print(len(self.result[:-1]))
		print(*self.result[:-1])

def main():
	N, M, cost_matrix, distance_matrix, Q = import_data()

	sol = Solver(N, M, cost_matrix, distance_matrix, Q)

	sol.solve()

	sol.print_sol()

if __name__ == "__main__":
	main()
