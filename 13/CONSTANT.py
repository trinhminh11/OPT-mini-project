# Room class, store ID and capacity 
class Room:
	def __init__(self, ID, capacity):
		self.ID = ID
		self.capacity = capacity
	
	def __str__(self):
		return f'ID: {self.ID}, capacity: {self.capacity}'

# Slot class, store a slot ID (1,2,3,4) and list of rooms used in that slot
class Slot:
	def __init__(self, ID):
		self.ID = ID
		self.used: list[Room] = []

# Class class, represent a Class, with number of students, list of all Class share the same Course and list of room that can used for the exam
class Class:
	def __init__(self, ID, num_student):
		self.ID = ID
		self.num_student = num_student

		self.share_course: list[Class] = []
		
		self.rooms: list[Room] = []

		self.exam = None 
		self.slot = None
	
#import data
def import_data(file):
	classes: list[Class] = []
	rooms: list[Room] = []
	with open(file, 'r') as f:
		N, M = map(int, f.readline().split())
		temp = list(map(int, f.readline().split()))

		for i in range(N):
			classes.append(Class(i+1, temp[i]))
		
		temp = list(map(int, f.readline().split()))

		for i in range(M):
			rooms.append(Room(i+1, temp[i]))
		
		K = int(f.readline())

		for _ in range(K):
			i, j = map(int, f.readline().split())
			if classes[j-1] not in classes[i-1].share_course:
				classes[i-1].share_course.append(classes[j-1])
			if classes[i-1] not in classes[j-1].share_course:
				classes[j-1].share_course.append(classes[i-1])
	
	return classes, rooms