class Thesis:
	def __init__(self, ID):
		self.ID = ID

		self.teacher: Teacher = None
		
		self.council = 0

class Teacher:
	def __init__(self, ID):
		self.ID = ID

		# number of student that this teacher guide
		self.load = 0

		# list of thesis that this teacher guide
		self.thesises: list[int] = []

		self.council = 0
		
		self.min_similarity: dict[Teacher, int] = {}

class Council:
	def __init__(self, ID):
		self.ID = ID

		self.load = 0

		self.thesises: list[Thesis] = []
		self.teachers: list[Teacher] = []

def import_data(inp):
	s = []
	g = []
	with open(inp, 'r') as file:
		N, M, K = map(int, file.readline().split())

		thesises = [Thesis(i+1) for i in range(N)]
		teachers = [Teacher(i+1) for i in range(M)]
		councils = [Council(i+1) for i in range(K)]


		a, b, c, d, e, f = map(int, file.readline().split())


		for _ in range(N):
			s.append(list(map(int, file.readline().split())))
		
		for _ in range(N):
			g.append(list(map(int, file.readline().split())))
		
		t = list(map(int, file.readline().split()))

		for i in range(N):
			thesises[i].teacher = teachers[t[i]-1]
			teachers[t[i]-1].load += 1
			teachers[t[i]-1].thesises.append(i+1)

		
		for t1 in range(M):
			for t2 in range(t1+1, M):
				teacher1 = teachers[t1]
				teacher2 = teachers[t2]

				teacher1.min_similarity[teacher2] = float('inf')

				for i1 in range(len(teacher1.thesises)):
					s1 = teacher1.thesises[i1]
					for i2 in range(len(teacher2.thesises)):
						s2 = teacher2.thesises[i2]
						if teacher1.min_similarity[teacher2] > s[s1-1][s2-1] and s1 != s2 and s[s1-1][s2-1] > 0:
							teacher1.min_similarity[teacher2] = s[s1-1][s2-1]
				
				teacher2.min_similarity[teacher1] = teacher1.min_similarity[teacher2]
	
	return thesises, teachers, councils, a, b, c, d, e, f, s, g