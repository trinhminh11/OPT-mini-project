import random
from copy import deepcopy
from CONSTANT import import_data, random_seed, Council
import numpy as np
from scipy.optimize import linear_sum_assignment
import timeit

random.seed(random_seed)

'''
encode chromosome:
	- chromosome is a list with length = N
	- each gene is a number in range [1, K] represent Council of that student
decode chromosome:
	- for each gene in chromosome, add that council[gene]'s student add gene_index
	- loop through each council, calc similarity between student, return 0 if no sastified constrain >= e
	- loop through each council, create teachers matrix that each row represent each council, each column represent the total similarity of that teacher in council
	- using hungarian algorithm to choose teacher to add to each council
	- fitness is the total similarity of council that have minimum total similarity
'''

class Individual:
	def __init__(self, a,b,c,d,e,f, s, g, councils: list[Council], chromosome = None):

		#len of chromosome
		self.a = a
		self.b = b
		self.c = c
		self.d = d 
		self.e = e
		self.f = f
		self.s = s
		self.g = g
		self.councils = deepcopy(councils)
		self.n = len(s)

		#if chromosome = None, create random solution
		if chromosome == None:
			self.chromosome = [random.randint(1, len(councils)) for _ in range(self.n)]

		else:
			self.chromosome = chromosome

		self.fitness = 0

		self.prob = 0
	
	# add student to council base on chromosome
	def calc_sol(self):
		for i, gene in enumerate(self.chromosome):
			self.councils[gene-1].students.append(i+1)

	
	def calc_fitness(self):
		self.calc_sol()
		# fitness i represent total similarity of council i
		fitnesses = [0 for _ in range(len(self.councils))]

		for council in self.councils:
			# unsastisfied constraint
			if not (self.a <= len(council.students) <= self.b):
				return 0
			
			student_similarity = council.calc_student_similarity(self.e)

			# unsastisfied constraint
			if student_similarity == False:
				return 0
			
			# only 1 student
			elif student_similarity == -1:
				fitnesses[council.ID-1] += 0
			else:
				fitnesses[council.ID-1] += student_similarity
		
		
		
		num_teach = 0
		# need to add all teacher to council
		while num_teach < len(self.g[0]):
			teachers_matrix = []

			# calc teachers matrix
			for council in self.councils:
				teachers = {i: 0 for i in range(1, len(self.g[0])+1)}
				
				for teacher in range(1, len(self.g[0])+1):
					for student in council.students:
						if self.g[student-1][teacher-1] < self.f or teacher in council.teachers:
							teachers[teacher] = -1
						

						if teachers[teacher] != -1:
							teachers[teacher] += self.g[student-1][teacher-1]
				
				teachers_matrix.append(list(teachers.values()))

			# start hungarian using numpy and linear sum assignment

			cost_matrix = np.array(teachers_matrix)

			cost_matrix = -cost_matrix

			# if all teacher have similarity = -1, meaning can't add teacher -> return 0
			if cost_matrix.sum() == len(self.councils) * len(self.g[0]):
				return 0

			# Apply the Hungarian algorithm
			row_indices, col_indices = linear_sum_assignment(cost_matrix)

			for i, j in zip(row_indices, col_indices):

				if teachers_matrix[i][j] != -1:
					self.councils[i].teachers.append(j+1)
					num_teach += 1
					fitnesses[self.councils[i].ID-1] += teachers_matrix[i][j]

		# check teacher's constraint
		for council in self.councils:
			if not (self.c <= len(council.teachers) <= self.d):
				return 0 

		return min(fitnesses)
		

	
	#Crossover
	def crossover(self, other):
		mom_chromosome, dad_chromosome = random.sample([self.chromosome, other.chromosome], 2)

		return mom_chromosome[:self.n//2] + dad_chromosome[self.n//2:]
	
	#mutation
	def mutation(self, rate):
		if random.random() < rate:
			#choose mutation type
			choice = random.randint(0, self.n-1)

			self.chromosome[choice] = random.randint(1, len(self.councils))

#Solution class	
class GA:
	def __init__(self, a,b,c,d,e,f, s, g, councils, n, generations, mutation_rate):
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.e = e
		self.f = f
		self.s = s
		self.g = g
		self.councils = councils
		#Populations contain n Individual
		self.populations: list[Individual] = [Individual(a, b, c, d, e, f, s, g, councils) for _ in range(n)]
		self.n = n
		self.generations = generations
		self.mutation_rate = mutation_rate
	
	def solve(self):

		self.calc_fitness()

		# note that populations[-1] is the best individual

		#initial best solution is populations[-1]
		self.best_sol = self.populations[-1]


		
		iteration = 0
		max_iteration = 50

		#run for ... generations
		for generation in range(self.generations):
			iteration += 1
			Probs = self.calc_fitness()

			if self.populations[-1].fitness > self.best_sol.fitness:
				self.best_sol = self.populations[-1]


				iteration = 0

			
			# early stopping
			if iteration > max_iteration or timeit.default_timer() - start_time >= max_runtime:
				break

			new_gen = []

			# create new popultions
			for i in range(self.n):

				# choose parent
				parent: list[Individual] = self.natural_selection(Probs)

				# cross over
				child_chromosome = parent[0].crossover(parent[1])

				child = Individual(self.a, self.b, self.c, self.d, self.e, self.f, self.s, self.g, self.councils, child_chromosome)

				#mutation
				child.mutation(self.mutation_rate)


				#add new gen
				new_gen.append(child)
		
			self.populations = new_gen
		
		
	
	#calc populations fitness
	def calc_fitness(self):
		for indiviudal in self.populations:
			indiviudal.fitness = indiviudal.calc_fitness()

		#sort in increasing order of fitness
		self.populations.sort(key=lambda x: x.fitness)

		#rank selection
		sp = 1.2
		Probs = [1/self.n * (sp - (2*sp-2)*(i-1)/(self.n-1)) for i in range(1, self.n+1)]
		Probs.reverse()
		
		for i, individual in enumerate(self.populations):
			individual.prob = Probs[i]
		

		for i in range(1, len(Probs)):
			Probs[i] += Probs[i-1]
			
		return Probs

	
	#choose 2 parents base on rank
	def natural_selection(self, Probs):
		
		parent = []
		Probs = [0] + Probs

		for i in range(2):
			choice = random.uniform(0, Probs[-1])

			for i in range(1, len(Probs)):
				if Probs[i-1] <= choice <= Probs[i]:
					parent.append(self.populations[i-1])
					break

		return parent

	#printing solution
	def print_sol(self):
		ans_student = [0 for i in range(len(self.s))]
		ans_teacher = [0 for i in range(len(self.g[0]))]
		for council in self.best_sol.councils:
			for student in council.students:
				ans_student[student-1] = council.ID

			for teacher in council.teachers:
				ans_teacher[teacher-1] = council.ID
		
		print(len(ans_student))
		print(*ans_student)
		print(len(ans_teacher))
		print(*ans_teacher)


	
	def export_sol(self, file):
		ans_student = [0 for i in range(len(self.s))]
		ans_teacher = [0 for i in range(len(self.g[0]))]
		for council in self.best_sol.councils:
			for student in council.students:
				ans_student[student-1] = council.ID

			for teacher in council.teachers:
				ans_teacher[teacher-1] = council.ID

		with open(file, 'w') as f:
			f.write(f'{len(ans_student)}\n')
			for student in ans_student:
				f.write(f'{student} ')
			f.write("\n")

			f.write(f'{len(ans_teacher)}\n')
			for teacher in ans_teacher:
				f.write(f'{teacher} ')
			f.write("\n")
	


def main(inp, out):
	a,b,c,d,e,f, s, g, councils = import_data(inp)
	
	sol = GA(a,b,c,d,e,f,s,g,councils,100,100,0.01)

	sol.solve()

	sol.print_sol()

	sol.export_sol(out)

if __name__ == "__main__":
	start_time = timeit.default_timer()
	max_runtime = 30

	test_case = 3
	inp = f'input//{test_case}.txt'
	out = f'output//{test_case}.txt'
	main(inp, out)