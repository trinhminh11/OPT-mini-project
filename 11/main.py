import random
from CONSTANT import import_data, random_seed
random.seed(random_seed)

'''
encode chromosome:
	- chromosome is a permutation of [-K+1, -K+2, ..., 0, 1, 2, .., N], length of K + N
	- where [-K+1, -K+2, .., 0] represent truck and [1,2,3,..., N] represent Node
	or gene <= 0 represent truck and gene > 0 represent Node
	- note that chromosome allways start at -K+1 so in the actual code,
	chromosome is a permutation of [-K+2, -K+3, ..., 0, 1, 2, ..., N] length of K + N - 1
decode chromosome:
	- loop through chromosome, when gene <= 0 that mean we go to next truck and all node > 0 after that is the Route of that truck
'''

class Individual:
	def __init__(self, N, K, distance_matrix: list[list], chromosome = None):

		self.N = N 
		self.K = K
		#len of chromosome
		self.n = N + K - 1

		#if chromosome = None, create random solution
		if chromosome == None:
			self.chromosome = [-i for i in range(K-1)]
			self.chromosome += [i+1 for i in range(N)]
			random.shuffle(self.chromosome)
			
		else:
			self.chromosome = chromosome


		self.distance_matrix = distance_matrix

		self.fitness = 0


		self.prob = 0

	
	# calc fitness base on Route
	def calc_fitness(self):

		# Routes i represent truck {i+1} Route
		self.Routes = [[] for _ in range(self.K)]

		# start at the first truck
		index = 0
		self.Routes[0].append(0)

		for gene in self.chromosome:
			#if gene <= 0, go to next truck
			if gene <= 0:			
				index += 1
				#truck allways start at index 0
				self.Routes[index].append(0)
			else:
				self.Routes[index].append(gene)


		#fitness i represent cost of truck {i+1}
		fitnesses = [0 for _ in range(self.K)]
		for i, route in enumerate(self.Routes):
			for j in range(1, len(route)):
				fitnesses[i] += self.distance_matrix[route[j-1]][route[j]]
			
		
		
		#total fitness and max fitness
		return max(fitnesses), sum(fitnesses)
	
	#Crossover
	def crossover(self, other):
		choice = random.choice([1, 2, 3])
		if choice == 1:
			return self.OX(other)
		elif choice == 2:
			return self.ERX(other)
		else:
			return self.AEX(other)

	# Order cross over
	def OX(self, other):
		mom_chromosome = self.chromosome
		dad_chromosome = other.chromosome


		a = random.randint(1, self.n-1)
		b = random.randint(1, self.n-1)

		if a > b:
			a, b = b, a
		
		middle_chromosome: list = dad_chromosome[a:b]

		temp_chromosome: list = mom_chromosome[b:] + mom_chromosome[:b]

		for gene in middle_chromosome:
			temp_chromosome.remove(gene)

		child_chromosome = temp_chromosome[self.n-b:] + middle_chromosome + temp_chromosome[:self.n-b]
		
		return child_chromosome
	
	#Edge recombination crossover
	def ERX(self, other):
		mom_chromosome = self.chromosome
		dad_chromosome = other.chromosome

		def find_neighbor(gene):
			neighbors = []
			mom_index = mom_chromosome.index(gene)
			dad_index = dad_chromosome.index(gene)

			if mom_index == 0:
				neighbors += [mom_chromosome[-1], mom_chromosome[1]]

			elif mom_index == self.n-1:
				neighbors += [mom_chromosome[0], mom_chromosome[self.n-2]]
			
			else:
				neighbors += [mom_chromosome[mom_index-1], mom_chromosome[mom_index+1]]
			
			if dad_index == 0:
				neighbors += [dad_chromosome[-1], dad_chromosome[1]]

			elif dad_index == self.n-1:
				neighbors += [dad_chromosome[0], dad_chromosome[self.n-2]]
			
			else:
				neighbors += [dad_chromosome[dad_index-1], dad_chromosome[dad_index+1]]
			
			return list(set(neighbors))

		neighbors = {i: find_neighbor(i) for i in range(-self.K+2, self.N+1)}
		
		index = 0
		child_chromosome = []
		gene = mom_chromosome[0]
		while len(child_chromosome) < self.n:
			child_chromosome.append(gene)

			neighs = neighbors[gene]

			neighs.sort(key= lambda x: len(neighbors[x]))

			check = False
			for g in neighs:
				if g not in child_chromosome:
					gene = g
					check = True
					break
			
			if not check:
				for g in mom_chromosome:
					if g not in child_chromosome:
						gene = g
						break

		return child_chromosome

	# Alternating Edges cross over
	def AEX(self, other):
		mom_chromosome: list =  self.chromosome
		dad_chromosome: list = other.chromosome
		child_chromosome = []

		visited = {i: False for i in range(-self.K+1, self.N+1)}

		visited[-self.K+1] = True

		current = mom_chromosome

		index = 0

		while len(child_chromosome) < self.n:
			gene = current[index]
			child_chromosome.append(gene)
			visited[gene] = True

			if current == mom_chromosome:
				current = dad_chromosome
			elif current == dad_chromosome:
				current = mom_chromosome
			
			index = current.index(gene) + 1

			if index >= self.n:
				for i in range(-self.K+1, self.N+1):
					if visited[i] == False:
						index = current.index(i)
						break
			
			elif visited[current[index]] == True:
				for i in range(-self.K+1, self.N+1):
					if visited[i] == False:
						index = current.index(i)
						break
		
		return child_chromosome
	
	#mutation
	def mutation(self, rate):
		if random.random() < rate:
			#choose mutation type
			choice = random.choice([1,2,3])
			if choice == 1:
				self.swap_mutation()
			elif choice == 2:
				self.scramble_mutation()
			else:
				self.inversion_mutation()

	#take 2 gene and swap
	def swap_mutation(self):
		a = random.randint(0, self.n-1)
		b = random.randint(0, self.n-1)

		self.chromosome[a], self.chromosome[b] = self.chromosome[b], self.chromosome[a]
	
	# take genes from a to b and scramble
	def scramble_mutation(self):
		a = random.randint(0, self.n-1)
		b = random.randint(0, self.n-1)
		if a  > b:
			a, b = b, a

		temp = self.chromosome[a:b].copy()
		random.shuffle(temp)
		
		self.chromosome = self.chromosome[:a] + temp + self.chromosome[b:]
	
	# take genes from a to b and inverse
	def inversion_mutation(self):
		a = random.randint(0, self.n-1)
		b = random.randint(0, self.n-1)
		if a > b:
			a, b = b, a

		temp = self.chromosome[a:b].copy()
		temp.reverse()
		
		self.chromosome = self.chromosome[:a] + temp + self.chromosome[b:]

#Solution class	
class GA:
	def __init__(self, N, K, distance_matrix: list[list], n, generations, mutation_rate):
		#Populations contain n Individual
		self.populations: list[Individual] = [Individual(N, K, distance_matrix) for _ in range(n)]
		self.n = n
		self.generations = generations
		self.distance_matrix = distance_matrix
		self.mutation_rate = mutation_rate
		self.N = N
		self.K = K
	
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

			# if populations[-1] fitness is smaller than best sol, update best sol
			if   self.populations[-1].fitness < self.best_sol.fitness:
				self.best_sol = self.populations[-1]

				iteration = 0

			
			# early stopping
			if iteration > max_iteration:
				break

			new_gen = []

			# create new popultions
			for i in range(self.n):

				# choose parent
				parent: list[Individual] = self.natural_selection(Probs)

				# cross over
				child_chromosome = parent[0].crossover(parent[1])

				child = Individual(self.N, self.K, self.distance_matrix, child_chromosome)

				#mutation
				child.mutation(self.mutation_rate)

				#add new gen
				new_gen.append(child)
		
			self.populations = new_gen
		
		
	
	#calc populations fitness
	def calc_fitness(self):
		#calc fitness for each individual
		for indiviudal in self.populations:
			indiviudal.fitness = indiviudal.calc_fitness()

		#sort in decreasing order of fitness, best fitness at lass
		self.populations.sort(reverse=True, key= lambda x: x.fitness)

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
		print(self.K)
		for truck in range(self.K):
			print(len(self.best_sol.Routes[truck]))
			print(*self.best_sol.Routes[truck])

	#exporting solution
	def export_sol(self, file):
		with open(file, 'w') as f:
			f.write(str(self.K) + "\n")

			for truck in range(self.K):
				f.write(str(len(self.best_sol.Routes[truck])) + "\n")

				for node in self.best_sol.Routes[truck]:
					f.write(str(node) + " ")
				
				f.write("\n")



def main():
	try:
		N, K, distance_matrix = import_data('11/test.txt')
	except:
		N, K, distance_matrix = import_data('test.txt')

	populations_num = 100
	generations = 100
	mutation_rate = 0.1

	sol = GA(N, K, distance_matrix, populations_num, generations, mutation_rate)

	sol.solve()

	sol.print_sol()
	try:
		sol.export_sol('11/output.txt')
	except:
		sol.export_sol('output.txt')

if __name__ == "__main__":
	main()