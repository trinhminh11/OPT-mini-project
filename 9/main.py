from CONSTANT import import_data, Box, Container
from copy import deepcopy

'''
Heuristic: First Fit Algorithm
	Step 1: Rotate all Box so that height < width and sort in decreasing order of height
	Step 2: Rotate all Container so that height > width and sort in decreasing order of area then height
	Step 3: loop through each box if can add box to container, create a level is a horizontal line to that container, else go to next container

encode solution:
	each container have container.boxes (dict type) key =  Box and value = coordinate of that Box

decode solution:
	if container is rotate, simply rotate all box in that container to give actual coordinate of each box
'''

# Solver class, solve the problem
class Solver:
	def __init__(self, boxes: list[Box], containers: list[Container]):
		self.boxes = boxes
		self.containers = containers

	# Step 1
	def rotating_box(self):
		for box in self.boxes:
			if box.width < box.height:
				box.rotate()
		
		self.boxes.sort(reverse=True, key= lambda x: x.height)
	
	# Step 2
	def rotating_containter(self):
		for container in self.containers:
			if container.width > container.height:
				container.rotate()
		
		self.containers.sort(reverse = True, key= lambda x: [x.height*x.width, x.height])
	
	# main solve
	def solve(self):
		self.rotating_box()
		self.rotating_containter()

			
		# Step 3
		self.best_containers = deepcopy(self.containers)
		self.best_boxes = deepcopy(self.boxes)
		best_cost = float('inf')
		
		# run through all containers[0:], containers[1:], containers[2:], ... And get the best result
		# to find that in case containers[0] have very high cost, and we just needs to use many container after that to get a lower cost
		for i in range(len(self.containers)):
			cost = 0
			temp_boxes = deepcopy(self.boxes)
			temp_container = deepcopy(self.containers)

			is_break = False
			for box in temp_boxes:
				index = i

				while index < len(temp_container):
					if temp_container[index].Insert(box):
						break
					else:
						index += 1
				else:
					if i != 0:
						is_break = True 
			
			if is_break:
				break
				

			for container in temp_container:
				if len(container.boxes) > 0:
					cost += container.cost
			
			if cost < best_cost:
				best_cost = cost
				self.best_containers = deepcopy(temp_container)
				self.best_boxes = deepcopy(temp_boxes)

		self.sol = self.to_sol(self.best_containers)
	
	# decode solution
	def to_sol(self, containers: list[Container]):
		sol = {i+1: [-1, -1, -1, -1] for i in range(len(self.boxes))}
		for container in containers:
			if len(container.boxes) > 0:
				if container.rotation:
					container.rotate()
					for box, coor in container.boxes.items():
						box.rotate()
						coor.reverse()
						sol[box.ID] = [container.ID, coor[0], coor[1], int(box.rotation)]

				else:
					for box, coor in container.boxes.items():
						sol[box.ID] = [container.ID, coor[0], coor[1], int(box.rotation)]

		return sol
	
	#printing tol
	def print_sol(self):
		
		for box, info in self.sol.items():
			print(box, *info)
			
	def export_sol(self, file):
		with open(file, 'w') as f:
			for boxID, info in self.sol.items():
				f.write(f'{boxID} {info[0]} {info[1]} {info[2]} {info[3]}\n')


def main():
	try:
		boxes, containers = import_data("9/test.txt")
	except:
		boxes, containers = import_data("test.txt")
	
	sol = Solver(boxes, containers)

	sol.solve()

	sol.print_sol()

	try:
		sol.export_sol('9/output.txt')
	except:
		sol.export_sol("output.txt")


if __name__ == "__main__":
	main()