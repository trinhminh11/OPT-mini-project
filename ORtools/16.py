from ortools.sat.python import cp_model

class Field:
	def __init__(self, ID, d, s, e):
		self.ID = ID
		self.product = d
		self.s = s
		self.e = e


def import_data():
	fields = []
	N, m, M = map(int, input().split())

	min_day = float('inf')
	max_day = float('-inf')
	for i in range(N):
		d, s, e = map(int, input().split())
		fields.append(Field(i+1, d, s, e))
		if s < min_day:
			min_day = s
		if e > max_day:
			max_day = e
	
		


	return fields, m, M, min_day, max_day


class Solver:
	def __init__(self, fields: list[Field], m, M, min_day, max_day):
		# Num Fields
		self.N = len(fields)
		self.fields = fields
		# lower bound
		self.lower_bound = m
		# upper bound
		self.upper_bound = M

		self.min_day = min_day
		self.max_day = max_day

		self.X = [{j: 0 for j in range(min_day, max_day+1)} for _ in range(self.N)]


	def solve(self):
		model = cp_model.CpModel()

		for i in range(self.N):
			self.fields[i].used = model.NewBoolVar('used')
			for j in range(self.min_day, self.max_day+1):
				self.X[i][j] = model.NewIntVar(0, 1, f'x{i}{j}')

				if j < self.fields[i].s or j > self.fields[i].e:
					model.Add(self.X[i][j] == 0)
			
			model.Add(sum(self.X[i].values()) == 1).OnlyEnforceIf(self.fields[i].used)
			model.Add(sum(self.X[i].values()) == 0).OnlyEnforceIf(self.fields[i].used.Not())

			# model.Add(sum(self.X[i].values()) == 1)
		
		for j in range(self.min_day, self.max_day + 1):
			model.Add(self.lower_bound <= sum([self.X[i][j] * self.fields[i].product for i in range(self.N)])).OnlyEnforceIf(self.fields[i].used)
			model.Add(					  sum([self.X[i][j] * self.fields[i].product for i in range(self.N)]) <= self.upper_bound).OnlyEnforceIf(self.fields[i].used)
			# model.Add(self.lower_bound <= sum([self.X[i][j] * self.fields[i].product for i in range(self.N)]))
			# model.Add(			sum([self.X[i][j] * self.fields[i].product for i in range(self.N)])  <= self.upper_bound)

			
		
		model.Maximize(sum([self.fields[i].used for i in range(self.N)]))

		solver = cp_model.CpSolver()

		solver.Solve(model)



		self.result = []

		for field in self.fields:
			if solver.Value(field.used):
				for j in range(self.min_day, self.max_day+1):
					if solver.Value(self.X[field.ID-1][j]) == 1:
						self.result.append([field.ID, j])
						break

	def print_sol(self):
		print(len(self.result))

		for result in self.result:
			print(*result)

def main():
	fields, m, M, min_day, max_day = import_data()

	sol = Solver(fields, m, M, min_day, max_day)

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()