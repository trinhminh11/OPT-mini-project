
# Teacher class represent a Teacher, contain ID and all subjects of that teacher
class Teacher:
	def __init__(self, ID, subjects: list[int]):
		self.ID = ID
		self.subjects = subjects

		# dictionary with key = slot, value = True if this teacher busy on that slot and False if this teacher free
		self.used = {i: False for i in range(1, 61)}
	
	# print for debug
	def __str__(self):
		ans = f'Teacher: {self.ID}, subjects = ['

		for subject in self.subjects[:-1]:
			ans += f'{subject}, '
		
		ans += f'{self.subjects[-1]}]'

		return ans

# Class class represent a Class, contain ID and all subjects that this class have to study
class Class:
	def __init__(self, ID, subjects: list[int]):
		self.ID = ID
		self.subjects = subjects

		# Possible teacher can teach this Class
		# dict with key = subjects, value = list of teacher can teach this subject
		self.teachers: dict[int, list[Teacher]] = {subject: [] for subject in self.subjects}

		self.sol: dict[int, list[int]] = {subject: [] for subject in self.subjects}

		self.sol_subject: dict[int, list[int]] = {s: 0 for s in subjects}

		self.used = {i: False for i in range(1, 61)}


	# print for debug
	def __str__(self):
		ans = f'Class: {self.ID}, subjects = ['

		for subject in self.subjects[:-1]:
			ans += f'{subject}, '
		
		ans += f'{self.subjects[-1]}]'

		return ans


# import data
def import_data(file):
	classes: list[Class] = []
	teachers: list[Teacher] = []

	with open(file, 'r') as f:
		T, N, M = map(int, f.readline().split())

		for i in range(N):
			temp = list(map(int, f.readline().split()))
			temp.pop()

			classes.append(Class(i+1, temp))
		
		for i in range(T):
			temp = list(map(int, f.readline().split()))
			temp.pop()

			teachers.append(Teacher(i+1, temp))
		
		temp = list(map(int, f.readline().split()))
		
		#dictionary key = subject ID, value = preiods
		subjects = {i+1: temp[i] for i in range(M)}
	
	return classes, teachers, subjects