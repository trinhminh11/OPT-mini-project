from CONSTANT import import_data, Class, Room, Teacher


# Solver class to solve the problem
class Solver:
	def __init__(self, classes: list[Class], teachers: dict[int, Teacher], rooms: list[Room]):
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

		self.classes.sort(key=lambda x: [len(x.rooms)])
		rclass = []
		for c in self.classes:
			for slot in range(1, 61):
				if slot + c.t > 61:
					continue
				for room in c.rooms:
					check = True
					for preiod in range(slot, slot + c.t):
						if room.used[preiod] == True or self.teachers[c.g].used[preiod]:
							check = False 
							break

					if check:
						c.sol = [slot, room.ID]
						for preiod in range(slot, c.t + slot):
							room.used[preiod] = True
							self.teachers[c.g].used[preiod] = True
						
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
		
	def export_sol(self, file):
		with open(file, 'w') as f:

			f.write(str(len(self.classes)) + "\n")

			for c in self.classes:
				f.write(f'{c.ID} {c.sol[0]} {c.sol[1]}\n')


def main():
	classes, teachers, rooms = import_data('10/test.txt')


	sol = Solver(classes, teachers, rooms)

	sol.solve()

	sol.print_sol()

	sol.export_sol('10/output.txt')

if __name__ == "__main__":
	main()