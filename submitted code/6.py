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
		self.thesises = []

		self.council = 0
		
		self.min_similarity = {}

class Council:
	def __init__(self, ID):
		self.ID = ID

		self.load = 0

		self.thesises = []
		self.teachers = []

def import_data():
	s = []
	g = []
	N, M, K = map(int, input().split())

	thesises = [Thesis(i+1) for i in range(N)]
	teachers = [Teacher(i+1) for i in range(M)]
	councils = [Council(i+1) for i in range(K)]


	a, b, c, d, e, f = map(int, input().split())


	for _ in range(N):
		s.append(list(map(int, input().split())))
	
	for _ in range(N):
		g.append(list(map(int, input().split())))
	
	t = list(map(int, input().split()))

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


class Solver:
	def __init__(self, thesises, teachers, councils, a, b, c, d, e, f, s, g):
		self.N = len(thesises)
		self.thesises = thesises
		self.M = len(teachers)
		self.teachers = teachers
		self.K =len(councils)
		self.councils = councils
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.e = e
		self.f = f
		self.s = s
		self.g = g

	# teacher to council
	def Teacher2Council(self):
		for teacher in self.teachers:
			best_council: int = -1
			candidate_councils = []

			for council in self.councils:
				check = True

				for thesis in council.thesises:
					if self.g[thesis.ID-1][teacher.ID-1] < self.f:
						check = False
						break
					if thesis.teacher == teacher:
						check = False 
						break
				
				for cteacher in council.teachers:
					if teacher.min_similarity[cteacher] < self.e or teacher.min_similarity[cteacher] < self.f:
						check = False
						break
				
				if check:
					candidate_councils.append(council.ID)

			best_council = min(candidate_councils, key= lambda x: self.councils[x-1].load)


			if best_council != -1:
				teacher.council = best_council
				self.councils[best_council-1].teachers.append(teacher)
				self.councils[best_council-1].load += teacher.load
	
	def Thesis2Council(self):
		for thesis in self.thesises:
			best_council: int = -1
			candidate_councils = []

			for council in self.councils:
				check = True

				for cthesis in council.thesises:
					if self.s[thesis.ID-1][cthesis.ID-1] < self.e:
						check = False
						break
				
				for teacher in council.teachers:
					if teacher == thesis.teacher:
						check = False
						break 
				
				if check:
					candidate_councils.append(council.ID)
			
			best_council = min(candidate_councils, key= lambda x: len(self.councils[x-1].thesises))

			if best_council != -1:
				thesis.council = best_council
				self.councils[best_council-1].thesises.append(thesis)
	
	
	def solve(self):
		self.Teacher2Council()
		self.Thesis2Council()

	def print_sol(self):
		print(self.N)

		for thesis in self.thesises:
			print(thesis.council, end = " ")
		print()
		print(self.M)

		for teacher in self.teachers:
			print(teacher.council, end = " ")
		
		print()
	


def main():
	thesises, teachers, councils, a, b, c, d, e, f, s, g = import_data()

	sol = Solver(thesises, teachers, councils, a, b, c, d, e, f, s, g)

	sol.solve()

	sol.print_sol()

if __name__ == "__main__":
	main()
