from CONSTANT import import_data, Class, Room, Slot


class Solver:
	def __init__(self, classes: list[Class], rooms: list[Room]):
		self.classes = classes
		self.rooms = rooms
		self.rooms.sort(key=lambda x: x.capacity)

		self.slots: list[Slot] = [Slot(i+1) for i in range(4)]

	def find_possible_rooms(self):
		for c in self.classes:
			for room in self.rooms:
				if room.capacity >= c.num_student:
					c.rooms.append(room)
				
	
	def solve(self):
		self.find_possible_rooms()
		self.classes.sort(key=lambda x: len(x.rooms))

		for c in self.classes:
			for room in c.rooms:

				check_room = False
				for slot in range(1, 5):
					if room not in self.slots[slot-1].used:
						check = True
						for c2 in c.share_course:
							if slot == c2.slot:
								check = False
								break
						
						if check:
							c.exam = room.ID 
							c.slot = slot
							self.slots[slot-1].used.append(room)
							check_room = True 
							break

					if check_room:
						break
		
		self.classes.sort(key= lambda x: x.ID)


	def print_sol(self):
		for c in self.classes:
			print(c.ID, c.slot, c.exam)
	
	def export_sol(self, file):
		with open(file, 'w') as f:
			for c in self.classes:
				f.write(f'{c.ID} {c.slot} {c.exam}\n')
	

def main():
	classes, rooms = import_data("13/test.txt")

	sol = Solver(classes, rooms)

	sol.solve()

	sol.print_sol()

	sol.export_sol('13/output.txt')

	

if __name__ == "__main__":
	main()