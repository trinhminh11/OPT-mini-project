from CONSTANT import import_data, Room, Class


def import_output(file):
	ans = []
	with open(file, 'r') as f:
		while True:
			temp = list(map(int, f.readline().split()))
			if temp == []:
				break
			ans.append(temp)

	return ans

def Checker(classes: list[Class], rooms: list[Room] , ans, slots: dict[int, dict[int, list[Class]]]):
	for ID, slot, room_ID in ans:

		current_class: Class = classes[ID-1]

		if current_class.num_student > rooms[room_ID-1].capacity:
			print(f"class {current_class.ID} number of student greater than room {rooms[room_ID-1].ID} capacity")
			exit()

		if slots[slot][room_ID][0] == True:
			print(f"slot {slot}, room {room_ID} is already used (class: {ID})")
			exit()


		slots[slot][room_ID][0] = True
		
		for c in slots[slot][room_ID][1:]:
			if c in current_class.share_course:
				print('false')
				exit()
		
		slots[slot][room_ID].append(current_class)

			

def main():
	classes, rooms = import_data("13/test.txt")
	ans = import_output("13/output.txt")

	slots = {i: {j+1: [False] for j in range(len(rooms))} for i in range(1, 5)}


	Checker(classes, rooms, ans, slots)


if __name__ == "__main__":
	main()