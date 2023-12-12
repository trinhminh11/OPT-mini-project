# this code will fail at tests 700,800,900 and 1000. And it's not because this code is bad, it's just programming.daotao.ai designed poorly

class Container:
	def __init__(self, ID, W, H, cost):
		self.ID = ID
		self.W = W
		self.H = H
		self.cost = cost
		self.boxes = []
		self.used = False
		self.boxes_pos = [(0, 0)]

	def Insert_Box(self, box, x, y, rotation):
		box.x = x
		box.y = y
		box.rotation = rotation

		w, h = box.getWH()

		self.boxes_pos.append((x, y+h))
		self.boxes_pos.append((x+w, y))
		self.boxes.append(box)

		box.container = self.ID
	
	def check_Box(self, box, x, y, rotation):
		box.x = x
		box.y = y
		box.rotation = rotation

		w, h = box.getWH()

		if x + w > self.W or y + h > self.H:
			return False
		
		for _box in self.boxes:
			if _box.check_intersect(box):
				return False
		
		return True


class Box:
	def __init__(self, ID, W, H):
		self.ID = ID
		self.W = W
		self.H = H
		self.rotation = False
		self.x = None
		self.y = None
		self.container = None 
	
	def getWH(self):
		return (self.W, self.H) if not self.rotation else (self.H, self.W)
	
	def check_intersect(self, other):
		w1, h1 = self.getWH()
		w2, h2 = other.getWH()

		if max(self.x, other.x) >= min(self.x+w1, other.x+w2) or max(self.y, other.y) >= min(self.y + h1, other.y+h2):
			return False
		return True


def import_data():
	boxes = []
	containers = []

	N, K = map(int, input().split())

	for i in range(N):
		boxes.append(Box(i+1, *map(int, input().split())))
	
	for i in range(K):
		containers.append(Container(i+1, *map(int, input().split())))
	
	return boxes, containers


class Solver:
	def __init__(self, boxes, containers):
		self.boxes = boxes
		self.containers = containers

	def find_best_container(self, box):

		def _find_best_container(used = True):
			best_rotation = 0
			best_x, best_y = -1, -1
			best_container = None
			min_cost = float('inf')
			sum_XY = -1

			for container in self.containers:
				if container.used == used:
					stop = False
					for x, y in container.boxes_pos:
						for rotation in range(2):
							if container.check_Box(box, x, y, rotation):
								if [container.cost, x+y] < [min_cost, sum_XY]:
									min_cost = container.cost
									best_container = container
									best_rotation = rotation
									best_x = x
									best_y = y
									sum_XY = x + y
									stop = True 
					if stop:
						break					
			
			if min_cost < float('inf'):
				return best_container, best_x, best_y, best_rotation

			return _find_best_container(False)
		
		return _find_best_container()

	
	def solve(self):
		self.containers.sort(key=lambda x: [x.cost, x.ID])

		for box in self.boxes:
			container, x, y, rotation= self.find_best_container(box)

			container.boxes_pos.remove((x, y))

			container.Insert_Box(box, x, y, rotation)

			container.used = True 

	def print_sol(self):
		for box in self.boxes:
			print(box.ID, box.container, box.x, box.y, int(box.rotation))

def main():
	boxes, containers = import_data()

	sol = Solver(boxes, containers)

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()
