import random
from CONSTANT import Node, import_data, random_seed

random.seed(random_seed)

#Nodes object represent ID of Node, earliest and latest time to serve and time to delivery package


class Individual:
	def __init__(self, Nodes, Time_matrix, chromosome = None):

		#len of chromosome
		self.n = len(Nodes[1:])

		#if chromosome = None, create random solution
		if chromosome == None:
			self.chromosome = [i+1 for i in range(len(Nodes[1:]))]
			random.shuffle(self.chromosome)

		else:
			self.chromosome = chromosome

		self.Nodes = Nodes
		
		#make solution base on chromosome
		self.solRoute: list[Node] = [Nodes[0]] + [Nodes[i] for i in self.chromosome]

		self.Time_matrix = Time_matrix

		self.fitness = 0

		self.prob = 0
	
	#update Route base on chromosome
	def update_sol(self):
		self.solRoute: list[Node] = [self.Nodes[0]] + [self.Nodes[i] for i in self.chromosome]
	
	# calc fitness base on Route
	def calc_fitness(self):
		current_time = self.solRoute[0].timeDone

		for i in range(len(self.solRoute)-1):
			current_time += self.Time_matrix[self.solRoute[i].ID][self.solRoute[i+1].ID]
			
			# if we arrived before Time Window, we can wait.
			if current_time < self.solRoute[i+1].e:
				current_time = self.solRoute[i+1].e + self.solRoute[i+1].d
				self.solRoute[i+1].timeDone = current_time

			#if we arrived inside the Time Window 
			elif self.solRoute[i+1].e <= current_time <= self.solRoute[i+1].l:
				current_time += self.solRoute[i+1].d
				self.solRoute[i+1].timeDone = current_time
			
			#if we arrived after Time Window, meaning violating the constraint
			else:
				# delete afterward Node and stop
				self.solRoute = self.solRoute[:i+1]
				break
		
		# fitness equal [num serve, runtime]
		return [len(self.solRoute),  self.solRoute[-1].timeDone]
	
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

		neighbors = [set()]
		neighbors += [find_neighbor(i) for i in range(1, self.n+1)]
		
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
		visited = [False for i in range(self.n+1)]

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
				for i in range(len(visited)):
					if visited[i] == False:
						index = current.index(i)
						break
			
			elif visited[current[index]] == True:
				for i in range(len(visited)):
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
			
class GA:
	def __init__(self, Nodes: list[Node], Time_matrix, n, generations, mutation_rate):
		self.populations: list[Individual] = [Individual(Nodes, Time_matrix) for _ in range(n)]
		self.n = n
		self.generations = generations
		self.Nodes = Nodes
		self.Time_matrix = Time_matrix
		self.mutation_rate = mutation_rate
	
	def solve(self):

		self.calc_fitness()

		# note that populations[-1] is the best individual

		#initial best solution is populations[-1]
		self.best_sol = self.populations[-1]

		iteration = 0
		max_iteration = 50

		for generation in range(self.generations):
			iteration += 1
			Probs = self.calc_fitness()

			# if populations[-1] number of serve is better than best sol, update best sol
			if self.populations[-1].fitness[0] > self.best_sol.fitness[0]:
				self.best_sol = self.populations[-1]

				iteration = 0

			# if populations[-1] and best sol have the same number of serve, update best sol if populations[-1] have less runtime than best sol
			elif self.populations[-1].fitness[0] == self.best_sol.fitness[0]:
				if self.populations[-1].fitness[1] < self.best_sol.fitness[1]:
					self.best_sol = self.populations[-1]
					iteration = 0
			
			# early stopping
			if self.best_sol.fitness[0] == len(self.Nodes) and iteration > max_iteration:
				break

			new_gen = []

			# create new popultions
			for i in range(self.n):

				# choose parent
				parent: list[Individual] = self.natural_selection(Probs)

				# cross over
				child_chromosome = parent[0].crossover(parent[1])

				child = Individual(self.Nodes, self.Time_matrix, child_chromosome)

				#mutation
				child.mutation(self.mutation_rate)

				#update solRoute 
				child.update_sol()

				new_gen.append(Individual(self.Nodes, self.Time_matrix, child_chromosome))
		
			self.populations = new_gen
		
		

	def calc_fitness(self):
		for indiviudal in self.populations:
			indiviudal.fitness = indiviudal.calc_fitness()

		#sort in increasing order of number of served and -runtime
		self.populations.sort(key=lambda x: [x.fitness[0], -x.fitness[1]])

		#rank selection
		sp = 1.2
		Probs = [1/self.n * (sp - (2*sp-2)*(i-1)/(self.n-1)) for i in range(1, self.n+1)]
		Probs.reverse()

		for i, individual in enumerate(self.populations):
			individual.prob = Probs[i]
		

		for i in range(1, len(Probs)):
			Probs[i] += Probs[i-1]
			
		return Probs

	
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

	def print_sol(self):
		print(len(self.best_sol.solRoute[1:]))
		for node in self.best_sol.solRoute[1:]:
			print(node.ID, end = " ")




def main():
	N, Nodes, Time_matrix = import_data('test.txt')

	populations_num = 100
	generations = 100
	mutation_rate = 0.1

	sol = GA(Nodes, Time_matrix, populations_num, generations, mutation_rate)

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()