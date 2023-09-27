
# Box class, contain ID, width and height of box
class Box:
	def __init__(self, ID, width, height):
		self.ID = ID 
		self.width = width
		self.height = height

		# False if not rotate, True if rotate 90 degree
		self.rotation = False
	
	# function to ratate the box
	def rotate(self):
		self.rotation = not self.rotation
		self.width, self.height = self.height, self.width

	# print for debug
	def __str__(self):
		return f'Box {self.ID}, width-height = {self.width}-{self.height}, rotation: {self.rotation}'
		# return f'Box {self.ID}, height-width = {self.height}-{self.width}, rotation: {self.rotation}'
	
	
# Container class, contain ID, width, height and cost of container
class Container:
	def __init__(self, ID, width, height, cost):
		self.ID = ID 
		self.width = width
		self.height = height
		self.cost = cost

		# is rotation
		self.rotation = False

		# dictionary with key = Box and value = coordinate
		self.boxes: dict[Box, list] = {}

		# level of container
		self.levels = [[0, height]]

		# dictionary with key = bottom of level, value = furthest x in that level
		self.furthest_x: dict[int] = {0: 0}


	# add box to the level
	def canAdd(self, box, level):
		# x is the furthest coor in this level
		x = self.furthest_x[level[0]]

		# if the height of the box doesn't exceed the top of this level and x + width of the box doesn't exceed with of container
		if box.height + level[0] <= level[1] and x + box.width <= self.width:

			# add box to container'boxes with coor = [x, level[0]]
			self.boxes[box] = [x, level[0]]

			# update furthest_x
			self.furthest_x[level[0]] = x + box.width

			# temp is list of bottom of all level
			temp = [self.levels[i][0] for i in range(len(self.levels))]

			# if new level in list of bottom of all level, don't create new level, if not create new level
			if level[0] + box.height not in temp:
				# new level have top is the top of this level
				self.levels.append([level[0] + box.height, level[1]])
				# update current level top equal to this level bottom
				level[1] = level[0] + box.height

				# if this is the last level
				if level == self.levels[-1]:
					# furthest_x of new level is 0
					self.furthest_x[level[0] + box.height] = 0

				# if this level is not the last, meaning that new level is insert
				else:
					# furthest_x of new level is x
					self.furthest_x[level[0] + box.height] = x
					
			return True

		return False
	
	# Function to insert box to container
	def Insert(self, box: Box):
		self.levels.sort(key=lambda x: x[0])

		#loop through each level
		for level in self.levels:
			# check if can add box to this level
			if self.canAdd(box, level):
				return True
			# if not, rotate the box and check again
			else:
				box.rotate()
				if self.canAdd(box, level):
					return True
				else:
					box.rotate()
	
		return False
	
	def rotate(self):
		self.rotation = not self.rotation
		self.width, self.height = self.height, self.width

		self.levels = [[0, self.height]]
		
	
	#print for debug
	def __str__(self):
		return f'Container {self.ID}, width-height = {self.width}-{self.height}, cost = {self.cost}'
		# return f'Container {self.ID}, height-width = {self.height}-{self.width}, cost = {self.cost}'


def import_data(file):
	boxes: list[Box] = []
	containers: list[Container] = []
	with open(file, 'r') as f:
		N, K = map(int, f.readline().split())
		for i in range(N):
			boxes.append(Box(i+1, *list(map(int, f.readline().split()))))
		
		for i in range(K):
			containers.append(Container(i+1, *list(map(int, f.readline().split()))))
	
	return boxes, containers