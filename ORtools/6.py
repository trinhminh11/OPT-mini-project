from ortools.sat.python import cp_model

def import_data():
	s = []
	g = []

	N, M, K = map(int, input().split())

	a, b, c, d, e, f = map(int, input().split())


	for _ in range(N):
		s.append(list(map(int, input().split())))
	
	for _ in range(N):
		g.append(list(map(int, input().split())))
	
	t = list(map(lambda x: int(x)-1, input().split()))

	
	return N, M, K, a, b, c, d, e, f, t, s, g


class Solver:
	def __init__(self, N, M, K, a, b, c, d, e, f, t, s, g):
		# num project
		self.N = N
		# num teacher
		self.M = M
		# num council
		self.K = K

		self.t = t 

		self.project_lower_bound = a
		self.project_upper_bound = b
		self.teacher_lower_bound = c
		self.teacher_upper_bound = d 

		self.min_project_similarity = e
		self.min_teacher_similarity = f
		
		# N * N
		self.s = s
		# N * M
		self.g = g

		self.X = [[0 for _ in range(self.N)] for _ in range(self.K)]

		self.Y = [[0 for _ in range(self.M)] for _ in range(self.K)]
	
	def solve(self):
		model = cp_model.CpModel()

		max_project_cost = sum([sum(self.s[i]) for i in range(self.N)])

		max_teacher_cost = sum([sum(self.g[i]) for i in range(self.N)])
		
		for i in range(self.K):
			for j in range(self.N):
				self.X[i][j] = model.NewIntVar(0, 1, f'x{i}{j}')

			for j in range(self.M):
				self.Y[i][j] = model.NewIntVar(0, 1, f'x{i}{j}')
		
		for i in range(self.K):
			model.Add(self.project_lower_bound <= sum(self.X[i]))
			model.Add(sum(self.X[i]) <= self.project_upper_bound)

			model.Add(self.teacher_lower_bound <= sum(self.Y[i]))
			model.Add(sum(self.Y[i]) <= self.teacher_upper_bound)

		for i in range(self.N):
			for j in range(self.N):
				if self.s[i][j] < self.min_project_similarity and self.s[i][j] != 0:
					for k in range(self.K):
						model.Add(self.X[k][i] + self.X[k][j] != 2)

			for j in range(self.M):
				if self.g[i][j] < self.min_teacher_similarity:
					for k in range(self.K):
						model.Add(self.X[k][i] + self.Y[k][j] != 2)
			
			for k in range(self.K):
				model.Add(self.X[k][i] + self.Y[k][self.t[i]] != 2)
		
		for i in range(self.N):
			model.Add(sum([self.X[k][i] for k in range(self.K)]) == 1)

		for i in range(self.M):
			model.Add(sum([self.Y[k][i] for k in range(self.K)]) == 1)
		
		project_cost = []
		teacher_cost = []

		for k in range(self.K):
			project_cost.append(model.NewIntVar(0, max_project_cost, ''))
			teacher_cost.append(model.NewIntVar(0, max_teacher_cost, ''))
			for i1 in range(self.N-1):
				for i2 in range(i1+1, self.N):
					temp = model.NewIntVar(0, max_project_cost, '')
					model.AddMinEquality(temp, [self.X[k][i1], self.X[k][i2]])
					project_cost[k] += temp * self.s[i1][i2]
			 
			for i in range(self.N):
				for j in range(self.M):
					temp = model.NewIntVar(0, max_teacher_cost, '')
					model.AddMinEquality(temp, [self.X[k][i], self.Y[k][j]])
					teacher_cost[k] += temp * self.g[i][j]

		
		model.Maximize(sum(project_cost) + sum(teacher_cost))

		solver = cp_model.CpSolver()

		solver.Solve(model)

		self.projects = [_ for _ in range(self.N)]
		self.teachers = [_ for _ in range(self.M)]

		for k in range(self.K):
			for i in range(self.N):
				if solver.Value(self.X[k][i]) == 1:
					self.projects[i] = k+1
			
			for i in range(self.M):
				if solver.Value(self.Y[k][i]) == 1:
					self.teachers[i] = k+1

	def print_sol(self):
		print(len(self.projects))
		print(*self.projects)
		print(len(self.teachers))
		print(*self.teachers)


def main():
	sol = Solver(*import_data())

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()