import timeit

random_seed = 11042004
# Teacher class represent a Teacher, contain ID and all subjects of that teacher
class Teacher:
	def __init__(self, ID, subjects):
		self.ID = ID
		self.subjects = subjects

		# dictionary with key = slot, value = True if this teacher busy on that slot and False if this teacher free
		self.used = [False for i in range(1, 61)]
	
	def reset(self):
		self.used = [False for i in range(1, 61)]
	
	# print for debug
	def __str__(self):
		ans = f'Teacher: {self.ID}, subjects = ['

		for subject in self.subjects[:-1]:
			ans += f'{subject}, '
		
		ans += f'{self.subjects[-1]}]'

		return ans

# Class class represent a Class, contain ID and all subjects that this class have to study
class Class:
	def __init__(self, ID, subjects):
		self.ID = ID
		self.subjects = subjects

		# Possible teacher can teach this Class
		# dict with key = subject, value = list of teacher can teach this subject
		self.teachers = {subject: [] for subject in self.subjects}

		# dict with key = subject, value = [start time slot that teacher assign to this class, teacher]
		self.sol = {s: [] for s in subjects}

		self.used = [False for i in range(1, 61)]


	# print for debug
	def __str__(self):
		ans = f'Class: {self.ID}, subjects = ['

		for subject in self.subjects[:-1]:
			ans += f'{subject}, '
		
		ans += f'{self.subjects[-1]}]'

		return ans

def find_possible_teachers(classes, teachers):
	for c in classes:
		for subject in c.subjects:
			for teacher in teachers:
				if subject in teacher.subjects:
					c.teachers[subject].append(teacher)
		


def import_data():
	classes = []
	teachers = []

	
	T, N, M = map(int, input().split())

	for i in range(N):
		temp = list(map(int, input().split()))
		temp.pop()


		classes.append(Class(i+1, temp))
	
	for i in range(T):
		temp = list(map(int, input().split()))
		temp.pop()

		teachers.append(Teacher(i+1, temp))
	
	temp = list(map(int, input().split()))
	
	#dictionary key = subject ID, value = preiods
	subjects = {i+1: temp[i] for i in range(M)}
	find_possible_teachers(classes, teachers)


	return classes, teachers, subjects

# Solver class to solve the problem
class Solver:
	def __init__(self, classes, teachers, subjects):
		self.classes = classes
		self.teachers = teachers
		self.subjects = subjects

		self.length = 0

	# main solve function
	'''
	Heuristic:
		sort classes based on 2 criteria:
			first is increasing order of number of teachers can teach {subject with minimum number of teachers can teach}
			second is number of subjects

		loop through each {class}, loop through each {subject}, loop through each {slot}[1, 60], and loop through each {teacher}
		in the next {subject preiods} slots: 
			if {teacher} hasn't taught any class, assign {teacher} to {class} to teach {subject} in those slots
	'''	
	def solve(self):
		# sorting
		for c in self.classes:
			c.subjects.sort(key=lambda x: len(c.teachers[x]))
		self.classes.sort(key = lambda x: [len(x.teachers[x.subjects[0]]), len(x.subjects)])

		# loop through each class
		for c in self.classes:
			# loop through each subject
			for subject in c.subjects:
				# loop through each slot
				for slot in range(1, 61):
					# out of range
					if slot + self.subjects[subject] > 61:
						break
					
					# loop through each teacher
					for teacher in c.teachers[subject]:

						for preiod in range(slot, slot + self.subjects[subject]):
							# if teacher or class is used, break and go to next teacher
							if teacher.used[preiod-1] or c.used[preiod-1]:
								break
						# if teacher and class are not being used, assign teacher to class
						else:
							c.sol[subject] = [slot, teacher.ID]

							for preiod in range(slot, slot + self.subjects[subject]):
								teacher.used[preiod-1] = True
								c.used[preiod-1] = True
							break

					# if class.sol[subject] have teacher assign to it in this time_slot, break and go to next subject
					if c.sol[subject] != []:
						self.length += 1
						break
					
		self.classes.sort(key=lambda x: x.ID)
						
	def print_sol(self):

		print(self.length)
		
		for c in self.classes:
			c.subjects.sort()
			for subject in c.subjects:
				if c.sol[subject] != []:
					print(c.ID, subject, *c.sol[subject])
	
def main():
	classes, teachers, subjects = import_data()
	
	sol = Solver(classes, teachers, subjects)

	sol.solve()

	sol.print_sol()
	

if __name__ == "__main__":
	main()
