# class Class represent a class, contain ID, t: number of preiods, g: teacher ID, s: number of student
class Class:
	def __init__(self, ID, t, g, s):
		self.ID = ID
		self.t = t
		self.g = g 
		self.s = s

		# list of possible room
		self.rooms = []

		self.sol = []
	
	# print for debug
	def __str__(self):
		return f'class {self.ID}, preiods: {self.t}, teach by {self.g}, number of student {self.s}'

# class Room represent a Room, contain ID and capacity
class Room:
	def __init__(self, ID, capacity):
		self.ID = ID
		self.capacity = capacity
		
		self.last_False = 1

		# list of slot that this room being used
		self.used = {slot: False for slot in range(1, 61)}
	
	def find_free(self):
		temp = list(self.used.values())[::-1]

		count = 0

		for preiod in temp:
			if preiod:
				return count
			count += 1
		
		return count

class Teacher:
	def __init__(self, ID):
		self.ID = ID

		# list of slot that this teacher teach
		self.used = {slot: False for slot in range(1, 61)}
	
	def find_free(self):
		temp = list(self.used.values())[::-1]

		count = 0

		for preiod in temp:
			if preiod:
				return count
			count += 1
		
		return count
	
	def __str__(self):
		return f'Teacher {self.ID}'


# import data
def import_data():
	classes = []
	teachers = {}
	rooms = []


	N, M = map(int, input().split())
	for i in range(N):
		t, g, s = map(int, input().split())

		classes.append(Class(i+1, t, g, s))

		if g not in teachers.keys():
			teachers[g] = Teacher(g)


	temp = list(map(int, input().split()))
	
	for i, capacity in enumerate(temp):
		rooms.append(Room(i+1, capacity))

	return classes, teachers, rooms

		


# Solver class to solve the problem
class Solver:
	def __init__(self, classes, teachers, rooms):
		self.classes = classes
		self.teachers = teachers
		self.rooms = rooms

	
	# find possible room for all Class
	def find_possible_rooms(self):
		for c in self.classes:
			for room in self.rooms:
				if room.capacity >= c.s:
					c.rooms.append(room)

	# main solve function
	'''
	Heuristic:
		sort classes in increasing order of the number of possible rooms of that class can be assigned
		loop through each class, loop through each slot [1, 60], and loop through each room 
		if the next {class.t} slots, the room hasn't been used and the teacher hasn't taught any class
		assign this class to those slots
	'''	
	def solve(self):
		self.find_possible_rooms()


		self.classes.sort(key=lambda x: [x.t])

		rclass = []
		for c in self.classes:
			for slot in range(1, 61):
				if slot + c.t > 61:
					continue

				
				for room in c.rooms:
					
					for preiod in range(slot, slot + c.t):
						if room.used[preiod] == True or self.teachers[c.g].used[preiod]:
							break
					else:

						c.sol = [slot, room.ID]
						for preiod in range(slot, c.t + slot):
							room.used[preiod] = True
							self.teachers[c.g].used[preiod] = True

						room.last_False = c.t + slot
						
						break 
				
				if c.sol != []:
					break
			
			if c.sol == []:
				rclass.append(c)

		for c in rclass:
			self.classes.remove(c)
		
		# reset classes
		self.classes.sort(key= lambda x: x.ID)



	
	# printing solution
	def print_sol(self):

		print(len(self.classes))
		for c in self.classes:
			print(c.ID, *c.sol)


def main():
	classes, teachers, rooms = import_data()


	sol = Solver(classes, teachers, rooms)

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()
