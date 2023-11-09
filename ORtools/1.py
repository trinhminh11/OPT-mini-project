from ortools.sat.python import cp_model

# class Staff represent ID of staff and list of days off of that staff
class Staff:
	def __init__(self, ID, dayoff):
		self.ID = ID
		self.dayoff: list[int] = dayoff
	
	#printing for debug
	def __str__(self):
		ans = f"Staff {self.ID}: "
		for day in self.dayoff:
			ans += f'{day} '
		
		return ans 


#import data
def import_data():
	#list of staff
	staff: list[Staff] = []
	#N: number of Staff, D: number of Day, each slot in each day have at least A Staff and at most B staff
	N, D, A, B = map(int, input().split())
	for i in range(N):
		F = list(map(int, input().split()))
		F.pop()
		staff.append(Staff(i+1, F))
	
	return staff, D, A, B


class Solver:
	def __init__(self, staff: list[Staff], D, A, B):
		self.staff = staff
		self.D = D
		self.A = A
		self.B = B

		# solution matrix
		self.X = [[_ for _ in range(D)] for _ in range(len(self.staff))]
	
	def solve(self):
		# cp model
		model = cp_model.CpModel()

		# Xk[i][j] = 1 if X[i][j] = k, otherwise Xk[i][j] = 0
		X1 = [[_ for _ in range(self.D)] for _ in range(len(self.staff))]
		X2 = [[_ for _ in range(self.D)] for _ in range(len(self.staff))]
		X3 = [[_ for _ in range(self.D)] for _ in range(len(self.staff))]
		X4 = [[_ for _ in range(self.D)] for _ in range(len(self.staff))]

		for i in range(len(self.staff)):
			for j in range(self.D):
				self.X[i][j] = model.NewIntVar(0, 4, f'x{i}{j}')

				X1[i][j] = model.NewIntVar(0, 1, f'x1{i}{j}')
				X2[i][j] = model.NewIntVar(0, 1, f'x2{i}{j}')
				X3[i][j] = model.NewIntVar(0, 1, f'x3{i}{j}')
				X4[i][j] = model.NewIntVar(0, 1, f'x4{i}{j}')

				b1 = model.NewBoolVar('b1')
				model.Add(self.X[i][j] == 1).OnlyEnforceIf(b1)
				model.Add(self.X[i][j] != 1).OnlyEnforceIf(b1.Not())
				model.Add(X1[i][j] == 1).OnlyEnforceIf(b1)
				model.Add(X1[i][j] == 0).OnlyEnforceIf(b1.Not())

				
				b2 = model.NewBoolVar('b2')
				model.Add(self.X[i][j] == 2).OnlyEnforceIf(b2)
				model.Add(self.X[i][j] != 2).OnlyEnforceIf(b2.Not())
				model.Add(X2[i][j] == 1).OnlyEnforceIf(b2)
				model.Add(X2[i][j] == 0).OnlyEnforceIf(b2.Not())

				b3 = model.NewBoolVar('b3')
				model.Add(self.X[i][j] == 3).OnlyEnforceIf(b3)
				model.Add(self.X[i][j] != 3).OnlyEnforceIf(b3.Not())
				model.Add(X3[i][j] == 1).OnlyEnforceIf(b3)
				model.Add(X3[i][j] == 0).OnlyEnforceIf(b3.Not())

				b4 = model.NewBoolVar('b4')
				model.Add(self.X[i][j] == 4).OnlyEnforceIf(b4)
				model.Add(self.X[i][j] != 4).OnlyEnforceIf(b4.Not())
				model.Add(X4[i][j] == 1).OnlyEnforceIf(b4)
				model.Add(X4[i][j] == 0).OnlyEnforceIf(b4.Not())
				
				# add dayoff
				if j+1 in self.staff[i].dayoff:
					model.Add(self.X[i][j] == 0)

		# add dayoff contraint
		for i in range(len(self.staff)):
			for j in range(self.D-1):
				b = model.NewBoolVar('b')
				model.Add(self.X[i][j] == 4).OnlyEnforceIf(b)
				model.Add(self.X[i][j] != 4).OnlyEnforceIf(b.Not())
				
				model.Add(self.X[i][j+1] == 0).OnlyEnforceIf(b)
		
		#add minimum and maximum shift in a Day contraint
		for j in range(self.D):
			model.Add(sum([X1[i][j] for i in range(len(self.staff))]) >= self.A)
			model.Add(sum([X1[i][j] for i in range(len(self.staff))]) <= self.B)

			model.Add(sum([X2[i][j] for i in range(len(self.staff))]) >= self.A)
			model.Add(sum([X2[i][j] for i in range(len(self.staff))]) <= self.B)

			model.Add(sum([X3[i][j] for i in range(len(self.staff))]) >= self.A)
			model.Add(sum([X3[i][j] for i in range(len(self.staff))]) <= self.B)

			model.Add(sum([X4[i][j] for i in range(len(self.staff))]) >= self.A)
			model.Add(sum([X4[i][j] for i in range(len(self.staff))]) <= self.B)

		# make span objective value = max of night shift
		obj_var = model.NewIntVar(0, self.D, "makespan")

		model.AddMaxEquality(obj_var, [sum(X4[i]) for i in range(len(self.staff))])

		model.Minimize(obj_var)

		self.solver = cp_model.CpSolver()

		self.solver.Solve(model)
	
	def print_sol(self):
		for i in range(len(self.staff)):
			for j in range(self.D):
				print(self.solver.Value(self.X[i][j]), end = " ")
			print()


def main():
	staff, D, A, B = import_data()

	sol = Solver(staff, D, A, B)

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()