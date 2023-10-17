import random, copy
from CONSTANT import Package, Truck, import_data, random_seed


random.seed(random_seed)

#Individual represent 1 Solution
'''
encode chromosome:
	- chromosome is a permutation of [1,2,3,..N]
	- each gene is a Package ID
decode chromosome:
	- loop through chromosome, starting with truck 1, keep adding Package until it passing upper bound, then go to next truck
	- for each truck, if lower_bound <= capcity <= upper_bound. cost is equal total Package.cost
	- fitness = total cost of all truck 
'''
class Individual:
	def __init__(self, packages: list[Package], trucks: list[Truck], chromosome = None):

		#len of chromosome
		self.n = len(packages)

		#if chromosome = None, create random solution
		if chromosome == None:
			self.chromosome = [i for i in range(len(packages))]
			random.shuffle(self.chromosome)

		else:
			self.chromosome = chromosome

		self.packages = [copy.deepcopy(packages[i]) for i in self.chromosome]

		self.trucks = copy.deepcopy(trucks)

		self.serve = 0

		self.fitness = 0
		
		self.prob = 0
	
	
	def make_Route(self):
		truck_index = 0
		package_index = 0
		while package_index < len(self.packages):
			package = self.packages[package_index]

			if self.trucks[truck_index].capacity + package.capacity > self.trucks[truck_index].upper_bound:
				truck_index += 1
				package_index -= 1
			else:
				self.trucks[truck_index].capacity += package.capacity
				self.trucks[truck_index].packages.append(package)

			if truck_index >= len(self.trucks):
				break

			package_index += 1
		
		for truck in self.trucks:	
			if truck.lower_bound <= truck.capacity <= truck.upper_bound:
				for package in truck.packages:
					truck.cost += package.cost
					self.fitness += package.cost

			else:
				truck.packages = []
		
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

		neighbors = [find_neighbor(i) for i in range(self.n)]
		
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
		visited = [False for i in range(self.n)]


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


#Solution class	
class GA:
	def __init__(self, packages: list[Package], trucks: list[Truck], n, generations, mutation_rate):
		#Populations contain n Individual
		self.populations: list[Individual] = []
		for _ in range(n):
			ind = Individual(packages, trucks)
			ind.make_Route()
			self.populations.append(ind)
		self.n = n
		self.generations = generations
		self.mutation_rate = mutation_rate

		self.packages = packages
		self.trucks = trucks
		
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

			# if populations[-1]'s fitness is better than best sol's fitness, update best sol
			if self.populations[-1].fitness > self.best_sol.fitness:
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

				child = Individual(self.packages, self.trucks, child_chromosome)

				#mutation
				child.mutation(self.mutation_rate)

				child.make_Route()

				#add new gen
				new_gen.append(child)
		
			self.populations = new_gen
		
		self.best_sol.packages.sort(key=lambda x: x.ID)
		for truck in self.best_sol.trucks:
			if truck.cost > 0:
				for package in truck.packages:
					package.truck_used = truck
		
		
	
	#calc populations fitness
	def calc_fitness(self):

		#sort in increasing order of number of served and -runtime
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
		total = 0
		ans = ""
		for package in self.best_sol.packages:
			if package.truck_used.ID:

				ans += f'{package.ID} {package.truck_used.ID}\n'
				total += 1
		
		print(total)
		print(ans)
		

	
	def export_sol(self, file):
		total = 0
		ans = ""
		for package in self.best_sol.packages:
			if package.truck_used.ID:

				ans += f'{package.ID} {package.truck_used.ID}\n'
				total += 1

		with open(file, 'w') as f:
			f.write(f'{total}\n')
			f.write(ans)

def main(inp, out):
	packages, trucks = import_data(inp)
		
	trucks.sort(key = lambda x: x.lower_bound + (x.upper_bound - x.lower_bound)/2)
	n = 100
	generations = 100
	mutation_rate = 0.01



	sol = GA(packages, trucks, n, generations, mutation_rate)

	sol.solve()
	sol.print_sol()

	sol.export_sol(out)



if __name__ == "__main__":
	inp = f'test.txt'
	out = f'output.txt'
	main(inp, out)