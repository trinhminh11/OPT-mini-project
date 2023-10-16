from CONSTANT import import_data, Class, Teacher

# Solver class to solve the problem
class Solver:
	def __init__(self, classes: list[Class], teachers: list[Teacher], subjects: dict[int, int]):
		self.classes = classes
		self.teachers = teachers
		self.subjects = subjects

		self.length = 0

	
	# find possible teacher for all Class
	def find_possible_teachers(self):
		for c in self.classes:
			for subject in c.subjects:
				for teacher in self.teachers:
					if subject in teacher.subjects:
						c.teachers[subject].append(teacher)

			# sort subjects in increasing order of number of teach that can teach this subject			
			c.subjects.sort(key=lambda x: len(c.teachers[x]))
					

	# main solve function
	'''
	Heuristic:
		sort classes in increasing order of minimum len of teacher that can teach subject with minimum teacher can teach then length of subjects
		loop through each class, loop through each {subject}, loop through each {slot} [1, 60], and loop through each {teacher}
		if the next {subject preiods} slots, if {teacher} hasn't taught any class, assign {teacher} to {class} to teach {subject} in those slots
	'''	
	def solve(self):
		self.find_possible_teachers()

		# sort classes in increasing order of minimum len of teacher that can teach subject with minimum teacher can teach then length of subjects
		self.classes.sort(key = lambda x: [len(x.teachers[x.subjects[0]]), len(x.subjects)])

		for c in self.classes:
			for subject in c.subjects:
				for slot in range(1, 61):

					if slot + self.subjects[subject] > 61:
						continue

					for teacher in c.teachers[subject]:
						check = True	

						for preiod in range(slot, slot + self.subjects[subject]):
							if teacher.used[preiod] or c.used[preiod]:
								check = False 
								break
						
						if check:
							c.sol[subject] = [slot, teacher.ID]

							for preiod in range(slot, slot + self.subjects[subject]):
								teacher.used[preiod] = True
								c.used[preiod] = True

							break
					
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
	
	def export_sol(self, file):
		with open(file, 'w') as f:
			f.write(str(self.length) + "\n")

			for c in self.classes:
				c.subjects.sort()
				for subject in c.subjects:
					if c.sol[subject] != []:
						f.write(f'{c.ID} {subject} {c.sol[subject][0]} {c.sol[subject][1]}\n')


def main():
	try:
		classes, teachers, subjects = import_data('8/test.txt')
	except:
		classes, teachers, subjects = import_data('test.txt')
	
	sol = Solver(classes, teachers, subjects)

	sol.solve()

	sol.print_sol()

	try:
		sol.export_sol("8/output.txt")
	except:
		sol.export_sol("output.txt")

if __name__ == "__main__":
	main()