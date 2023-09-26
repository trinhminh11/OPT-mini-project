from CONSTANT import import_data, Class, Room, Slot


class Solver:
	def __init__(self, classes: list[Class], rooms: list[Room]):
		self.classes = classes
		self.rooms = rooms
		self.rooms.sort(key=lambda x: x.capacity)

		self.slots: list[Slot] = [Slot(i+1) for i in range(4)]

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
			for room in c.rooms:
				# check if this room used or not
				check_room = False
				for slot in range(1, 5):

					#if that slot is not used, check every share course
					if room not in self.slots[slot-1].used:
						check = True

						# check every share course
						for c2 in c.share_course:
							# if another Class share the same course, break
							if slot == c2.slot:
								check = False
								break
						# if all class doesn't share any course in this slot, meaning this class will take exam in this slot, room
						if check:
							c.exam = room.ID 
							c.slot = slot
							self.slots[slot-1].used.append(room)
							check_room = True 
							break
					
					# if this room is used, go to next slot
					if check_room:
						break
		
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
	

def main():
	classes, rooms = import_data("13/test.txt")

	sol = Solver(classes, rooms)

	sol.solve()

	sol.print_sol()

	sol.export_sol('13/output.txt')

	

if __name__ == "__main__":
	main()