

# class Class represent a class, contain ID, t: number of preiods, g: teacher ID, s: number of student
class Class:
	def __init__(self, ID, t, g, s):
		self.ID = ID
		self.t = t
		self.g = g 
		self.s = s

		# list of possible room
		self.rooms: list[Room] = []

		self.sol: list[int] = []
	
	# print for debug
	def __str__(self):
		return f'class {self.ID}, preiods: {self.t}, teach by {self.g}, number of student {self.s}'

# class Room represent a Room, contain ID and capacity
class Room:
	def __init__(self, ID, capacity):
		self.ID = ID
		self.capacity = capacity

		# list of slot that this room being used
		self.used: dict[int, bool] = {slot: False for slot in range(1, 61)}

class Teacher:
	def __init__(self, ID):
		self.ID = ID

		# list of slot that this teacher teach
		self.used: dict[int, bool] = {slot: False for slot in range(1, 61)}
	
	def __str__(self):
		return f'Teacher {self.ID}'


# import data
def import_data(file):
	classes: list[Class] = []
	teachers: dict[int, Teacher] = {}
	rooms: list[Room] = []


	with open(file, 'r') as f:
		N, M = map(int, f.readline().split())
		for i in range(N):
			t, g, s = map(int, f.readline().split())

			classes.append(Class(i+1, t, g, s))

			if g not in teachers.keys():
				teachers[g] = Teacher(g)


		temp = list(map(int, f.readline().split()))
		for i, capacity in enumerate(temp):
			rooms.append(Room(i+1, capacity))
	
	return classes, teachers, rooms

		