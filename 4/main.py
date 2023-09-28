import random
from CONSTANT import import_data, random_seed
random.seed(random_seed)

'''
encode chromosome:
	- chromosome is a permutaion of [1,2,3,...,N]
decode chromosome:
	- start at node 0 and go thorgh chromosome until sastisfied constraint, each gene in chromosome represent a node in Route
'''

class Individual:
	def __init__(self, N, M, cost_matrix, distance_matrix: list[list], q, chromosome = None):

		self.N = N 
		self.M = M
		self.cost_matrix = cost_matrix
		
		self.q = q
		#len of chromosome
		self.n = M
		

		#if chromosome = None, create random solution
		if chromosome == None:
			self.chromosome = [i+1 for i in range(M)]
			random.shuffle(self.chromosome)
			
		else:
			self.chromosome = chromosome


		self.distance_matrix = distance_matrix

		self.fitness = 0


		self.prob = 0

	
	# calc fitness base on Route
	def calc_fitness(self):
		# current cost of the Route
		current_cost = [0 for _ in range(self.N)]
		# Route of the Truck
		self.Route = []

		self.Route.append(0)
		
		for gene in self.chromosome:
			self.Route.append(gene)

			# count how many cost is greater than q
			count_pass = 0

			# if add to cose
			for i in range(self.N):
				current_cost[i] += self.cost_matrix[i][gene-1]
				if current_cost[i] > self.q[i]:		
					count_pass += 1
			
			# if all cost is greater than q => finishing Route
			if count_pass == self.N:
				break
		
		self.Route.append(0)
		#fitness of Route
		fitness = 0

		for i in range(1, len(self.Route)):
			fitness += self.distance_matrix[self.Route[i-1]][self.Route[i]]
			
		
		return fitness
	
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

		neighbors = {i: find_neighbor(i) for i in range(1, self.n+1)}
		
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

		visited = {i: False for i in range(self.n+1)}

		visited[0] = True

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
				for i in range(self.n+1):
					if visited[i] == False:
						index = current.index(i)
						break
			
			elif visited[current[index]] == True:
				for i in range(self.n+1):
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
	def __init__(self, N, M, cost_matrix, distance_matrix: list[list], q, n, generations, mutation_rate):
		#Populations contain n Individual
		self.populations: list[Individual] = [Individual(N, M, cost_matrix, distance_matrix, q) for _ in range(n)]
		self.n = n
		self.generations = generations
		self.distance_matrix = distance_matrix
		self.mutation_rate = mutation_rate
		self.N = N
		self.M = M
		self.cost_matrix = cost_matrix
		self.q = q

	
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
			if self.populations[-1].fitness < self.best_sol.fitness:
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

				child = Individual(self.N, self.M, self.cost_matrix, self.distance_matrix, self.q, child_chromosome)

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
		print(len(self.best_sol.Route)-2)
		print(*self.best_sol.Route[1:-1])

	#exporting solution
	def export_sol(self, file):
		with open(file, 'w') as f:
			f.write(f'{len(self.best_sol.Route)-2}\n')
			
			for node in self.best_sol.Route[1:-1]:
				f.write(str(node) + " ")



def main():
	try:
		N, M, cost_matrix, distance_matrix, q = import_data('4/test.txt')
	except:
		N, M, cost_matrix, distance_matrix, q  = import_data('test.txt')

	populations_num = 100
	generations = 100
	mutation_rate = 0.1

	sol = GA(N, M, cost_matrix, distance_matrix, q, populations_num, generations, mutation_rate)

	sol.solve()

	sol.print_sol()
	
	try:
		sol.export_sol('4/output.txt')
	except:
		sol.export_sol('output.txt')

if __name__ == "__main__":
	main()