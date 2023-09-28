
random_seed = 11042004

class Council:
	def __init__(self, ID, s, g):
		self.ID = ID
		self.s = s
		self.g = g

		self.students: list[int] = []

		self.teachers: list[int] = []
	
	def calc_similarity(self, e, f):
		a = self.calc_student_similarity(e)
		b = self.calc_teacher_similarity(f)
		if a and b:
			return a + b
		else:
			return False
	
	def calc_student_similarity(self, e):
		total_sim = 0

		if len(self.students) <= 1:
			return -1
		
		
		for i in range(len(self.students)-1):
			for j in range(i+1, len(self.students)):
				first_student = self.students[i]
				second_student = self.students[j]

				sim = self.s[first_student-1][second_student-1]


				if sim < e:
					return False
				
				total_sim += sim
		
		return total_sim

	def calc_teacher_similarity(self, f):
		total_sim = 0
		for student in self.students:
			for teacher in self.teachers:
				sim = self.g[student-1][teacher-1]
				if sim < f:
					return False
				total_sim += sim

		return total_sim
	
	
class Student:
	def __init__(self, ID, other_students: list):
		self.ID = ID
		self.other_students = other_students
		self.teachers:list[list] = []
	
	def __str__(self):
		return f'Student {self.ID}'
		



def import_data(file):
	s = []
	g = []
	with open(file, 'r') as fi:
		N, M, K = map(int, fi.readline().split())

		a, b, c, d, e, f = map(int, fi.readline().split())

		for i in range(N):
			s.append(list(map(int, fi.readline().split())))

		for i in range(N):
			g.append(list(map(int, fi.readline().split())))
		
		t = list(map(int, fi.readline().split()))

		for i in range(N):
			g[i][t[i]-1] = -1
			s[i][i] = -1
	
		
	councils = [Council(i+1, s, g) for i in range(K)]
		
	
	return a,b,c,d,e,f, s, g, councils