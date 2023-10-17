from CONSTANT import import_data, Class, Room, Slot


class Solver:
	def __init__(self, classes: list[Class], rooms: list[Room]):
		self.classes = classes
		self.rooms = rooms
		self.rooms.sort(key=lambda x: x.capacity)

		self.slots: list[Slot] = []

	# find possible room for all Class
	def find_possible_rooms(self):
		for c in self.classes:
			for room in self.rooms:
				if room.capacity >= c.num_student:
					c.rooms.append(room)
				
	# main solve
	def solve(self):
		self.find_possible_rooms()


		# sort classes base on how many possible room all there for that Class
		self.classes.sort(key=lambda x: len(x.rooms))

		# for every class in classes, run through all possible rooms, check every slot availble
		for c in self.classes:
			slot = 1
			while True:
				
				if slot > len(self.slots):
					self.slots.append(Slot(slot))
				
				for c2 in c.share_course:
					if slot == c2.slot:
						break
				else:
					check = False
					for room in c.rooms:
						if room not in self.slots[slot-1].used:
							c.exam = room.ID
							c.slot = slot
							self.slots[slot-1].used.append(room)
							check = True
							break
					if check:
						break

				slot += 1
		
		# reset classes
		self.classes.sort(key= lambda x: x.ID)

	#printing solution
	def print_sol(self):
		for c in self.classes:
			print(c.ID, c.slot, c.exam)
	
	#exporting solution
	def export_sol(self, file):
		with open(file, 'w') as f:
			for c in self.classes:
				f.write(f'{c.ID} {c.slot} {c.exam}\n')
	

def main(inp, out):
	classes, rooms = import_data(inp)

	sol = Solver(classes, rooms)

	sol.solve()

	sol.print_sol()

	sol.export_sol(out)

	

if __name__ == "__main__":
	inp = f'test.txt'
	out = f'output.txt'
	main(inp, out)