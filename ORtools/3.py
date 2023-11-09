from ortools.sat.python import cp_model

def import_data():
	q = []

	N, Q = map(int, input().split())
	for _ in range(Q):
		i, j = map(int, input().split())
		q.append([i-1, j-1])
	
	
	d = list(map(int, input().split()))
	
	M = int(input())

	c = [[-1 for _ in range(M)] for _ in range(N)]

	s = list(map(int, input().split()))

	if len(s) == M:
		K = int(input())
	else:
		K = s.pop()


	for _ in range(K):
		i, j, _c = map(int, input().split())
		c[i-1][j-1] = _c

	return N, q, d, M, s, c

class Solver:
	def __init__(self, N, q, d, M, s, c):
		# num task
		self.N = N
		# work matrix
		self.q = q
		# task duration
		self.d = d
		# num worker
		self.M = M
		# start time of worker
		self.s = s
		# cost matrix
		self.c = c
		
		# solution matrix
		self.X = [[0 for _ in range(M)] for _ in range(N)]

		# start time of job
		self.time = [0 for _ in range(N)]

		self.used = [0 for _ in range(N)]
	
	
	def solve(self):
		model = cp_model.CpModel()

		for i in range(self.N):
			for j in range(self.M):
				self.X[i][j] = model.NewIntVar(0, 1, f'x{i}{j}')

				if self.c[i][j] == -1:
					model.Add(self.X[i][j] == 0)
		
		max_time = max(self.s) + sum(self.d)

		max_cost = sum([max(max(self.c[i]), 0) for i in range(self.N)])


		for i in range(self.N):
			self.time[i] = model.NewIntVar(0, max_time, f'time {i}')
			model.Add(self.time[i] >= sum(self.s[j] * self.X[i][j] for j in range(self.M)))

			self.used[i] = model.NewIntVar(0, 1, f'used {i}')

			model.Add(sum(self.X[i]) == self.used[i])
		
		for j in range(self.M):
			for i1 in range(self.N-1):
				for i2 in range(i1+1, self.N):
					b = model.NewBoolVar('b')
					model.Add(self.X[i1][j] + self.X[i2][j] == 2).OnlyEnforceIf(b)
					model.Add(self.X[i1][j] + self.X[i2][j] != 2).OnlyEnforceIf(b.Not())

					model.Add(self.time[i1] != self.time[i2])

		
		for u, v in self.q:
			model.Add(self.time[v] >= self.time[u] + self.d[u])

		cost = [[self.X[i][j] * self.c[i][j] for j in range(self.M)] for i in range(self.N)]
		
		num_task_obj = sum(self.used)

		total_time_obj = model.NewIntVar(0, max_time, "total time")

		model.AddMaxEquality(total_time_obj, [self.time[i] + self.d[i] for i in range(self.N)])

		total_cost_obj = sum([sum(cost[i]) for i in range(self.N)])


		obj = num_task_obj*(max_time + 1)* ( max_cost + 1) - total_time_obj * (max_cost + 1) - total_cost_obj

		model.Maximize(obj)
		
		solver = cp_model.CpSolver()

		solver.Solve(model)

		self.result = []

		for i in range(self.N):
			for j in range(self.M):
				if solver.Value(self.X[i][j]) == 1:
					self.result.append([i+1, j+1, solver.Value(self.time[i])])


	def print_sol(self):
		print(len(self.result))
		for r in self.result:
			print(*r)

def main():
	sol = Solver(*import_data())

	sol.solve()

	sol.print_sol()

if __name__ == "__main__":
	main()
