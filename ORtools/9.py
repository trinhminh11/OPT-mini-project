from ortools.sat.python import cp_model

class Container:
	def __init__(self, W, H, cost):
		self.W = W
		self.H = H
		self.cost = cost

		self.used = None

class Box:
	def __init__(self, w, h):
		self.w = w
		self.h = h

		self.rotation = None
		self.True_w = None
		self.True_h = None

		self.x = None
		self.y = None
		

def import_data():
	boxes = []
	containers = []

	N, K = map(int, input().split())

	for _ in range(N):
		w, h = map(int, input().split())
		boxes.append(Box(w, h))

	for _ in range(K):
		W, H, c = map(int, input().split())
		containers.append(Container(W, H, c))

	return boxes, containers

class Solver:
	def __init__(self, boxes, containers):
		self.N = len(boxes)
		self.K = len(containers)

		self.boxes: list[Box] = boxes
		self.containers: list[Container] = containers

		# container i, box j
		self.X = [[0 for _ in range(self.N)] for _ in range(self.K)]


	def solve(self):
		model = cp_model.CpModel()

		min_WH = min(min(self.boxes, key=lambda x: x.w).w, min(self.boxes, key= lambda x: x.h).h)
		max_WH = max(max(self.boxes, key=lambda x: x.w).w, max(self.boxes, key= lambda x: x.h).h)
		container_max_WH = max(max(self.containers, key= lambda x: x.W).W, max(self.containers, key= lambda x: x.H).H)

		for k in range(self.K):
			self.containers[k].used = model.NewBoolVar(f'used {k}')

			for i in range(self.N):
				self.X[k][i] = model.NewIntVar(0, 1, f'x{k}{i}')
			
			# if used container i, number of box in container i must >= 1
			model.Add(sum(self.X[k]) >= 1).OnlyEnforceIf(self.containers[k].used)
			model.Add(sum(self.X[k]) == 0).OnlyEnforceIf(self.containers[k].used.Not())

		# used all boxes
		for i in range(self.N):
			model.Add(sum([self.X[k][i] for k in range(self.K)]) == 1)

		for i in range(self.N):
			# rotation
			self.boxes[i].rotation = model.NewBoolVar(f'o{i}')
			self.boxes[i].True_w = model.NewIntVar(min_WH, max_WH, f'box {i} true w')
			self.boxes[i].True_h = model.NewIntVar(min_WH, max_WH, f'box {i} true h')

			self.boxes[i].x = model.NewIntVar(0, container_max_WH, f'box {i} x')
			self.boxes[i].y = model.NewIntVar(0, container_max_WH, f'box {i} y')

			# get true W and true H base on rotation
			model.Add(self.boxes[i].True_w == self.boxes[i].w).OnlyEnforceIf(self.boxes[i].rotation.Not())
			model.Add(self.boxes[i].True_h == self.boxes[i].h).OnlyEnforceIf(self.boxes[i].rotation.Not())

			model.Add(self.boxes[i].True_w == self.boxes[i].h).OnlyEnforceIf(self.boxes[i].rotation)
			model.Add(self.boxes[i].True_h == self.boxes[i].w).OnlyEnforceIf(self.boxes[i].rotation)

			# bound of x
			model.Add(0 <= self.boxes[i].x)
			model.Add(self.boxes[i].x + self.boxes[i].True_w <= sum([self.X[k][i]*self.containers[k].W for k in range(self.K)]))

			# bound of y
			model.Add(0 <= self.boxes[i].y)
			model.Add(self.boxes[i].y + self.boxes[i].True_h <= sum([self.X[k][i]*self.containers[k].H for k in range(self.K)]))


		for i1 in range(self.N-1):
			for i2 in range(i1+1, self.N):
				max_lower_left_x = model.NewIntVar(0, container_max_WH, '')
				min_upper_right_x = model.NewIntVar(0, container_max_WH, '')
				max_lower_left_y = model.NewIntVar(0, container_max_WH, '')
				min_upper_right_y = model.NewIntVar(0, container_max_WH, '')

				model.AddMaxEquality(max_lower_left_x, [self.boxes[i1].x, self.boxes[i2].x])
				model.AddMinEquality(min_upper_right_x, [self.boxes[i1].x + self.boxes[i1].True_w, self.boxes[i2].x + self.boxes[i2].True_w])
				model.AddMaxEquality(max_lower_left_y, [self.boxes[i1].y, self.boxes[i2].y])
				model.AddMinEquality(min_upper_right_y, [self.boxes[i1].y + self.boxes[i1].True_h, self.boxes[i2].y + self.boxes[i2].True_h])

				b1 = model.NewBoolVar('')
				b2 = model.NewBoolVar('')

				# if max_lower_left_x >= min_upper_right_x or max_lower_left_y >= min_upper_right_y => no overlap
				model.Add(max_lower_left_x >= min_upper_right_x).OnlyEnforceIf(b1)
				model.Add(max_lower_left_y >= min_upper_right_y).OnlyEnforceIf(b2)
				
				# else, overlap
				model.Add(max_lower_left_x < min_upper_right_x).OnlyEnforceIf(b1.Not())
				model.Add(max_lower_left_y < min_upper_right_y).OnlyEnforceIf(b2.Not())

				# if used i1 and i2 => b1 or b2
				for k in range(self.K):
					model.AddBoolOr(b1, b2).OnlyEnforceIf(self.X[k][i1], self.X[k][i2])

		
		model.Minimize(sum([self.containers[k].cost * self.containers[k].used for k in range(self.K)]))

		solver = cp_model.CpSolver()

		solver.Solve(model)

		self.result = [_ for _ in range(self.N)]

		for i in range(self.N):
			for k in range(self.K):
				if solver.Value(self.X[k][i]) == 1:
					self.result[i] = [i+1, k+1, solver.Value(self.boxes[i].x), solver.Value(self.boxes[i].y), solver.Value(self.boxes[i].rotation)]
					break
					
	def print_sol(self):
		for result in self.result:
			print(*result)


def main():
	sol = Solver(*import_data())

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()

