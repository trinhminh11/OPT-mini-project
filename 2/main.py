from CONSTANT import import_data, Truck, Package, Process, random_seed
from copy import deepcopy
import random

random.seed(random_seed)

'''
encode:
	- chromosome have length = length of packages
decode:
	- each gene in chromosome represent the truck (gene) that delivery package (gene's index)
	- loop through truck, loop through packages of that truck, Insert package to truck

fitness = max(truck.runtime), sum(truck.runtime)

'''
class Individual:
	def __init__(self, trucks: list[Truck], packages: list[Package], chromosome = None):
		# len of chromosome
		self.n = len(packages)
		if chromosome == None:
			self.chromosome = [random.randint(1, len(trucks)) for _ in range(self.n)]
		else:
			self.chromosome = chromosome
		
		self.trucks = deepcopy(trucks)
		self.packages = deepcopy(packages)

		self.fitness = 0
	
	# decode
	def decode(self):
		for truck in self.trucks:
			truck.packages = []
			truck.solRoute = [Process(0, 0, 0, True), Process(0, 0, 0, False)]
			truck.solRoute[-1].timeDone = 0

		for i in range(len(self.chromosome)):
			self.trucks[self.chromosome[i]-1].packages.append(self.packages[i])
	
	# solve for route
	def solve(self):
		self.decode()
		for truck in self.trucks:
			for package in truck.packages:
				truck.Insert(package)
	
	# calc fitness
	def calc_fitness(self):
		self.solve()
		fitnesses = [0 for i in range(len(self.trucks))]

		for truck in self.trucks:
			fitnesses[truck.ID-1] = truck.solRoute[-1].timeDone
		
		return max(fitnesses), sum(fitnesses)
	
	# normal crossover
	def crossover(self, other):
		mom_chromosome, dad_chromosome = random.sample( [self.chromosome, other.chromosome] , 2)

		return mom_chromosome[:self.n//2] + dad_chromosome[self.n//2:]
	
	#mutation
	def mutation(self, rate):
		if random.random() < rate:
			choice = random.randint(0, self.n-1)
			
			self.chromosome[choice] = random.randint(1, len(self.trucks))
	
class GA:
	def __init__(self, trucks, packages, n, generations, mutation_rate):
		self.trucks = trucks
		self.packages = packages
		#Populations contain n Individual
		self.populations: list[Individual] = [Individual(trucks, packages) for _ in range(n)]
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

				child = Individual(self.trucks, self.packages, child_chromosome)

				#mutation
				child.mutation(self.mutation_rate)

				#add new gen
				new_gen.append(child)
		
			self.populations = new_gen
		
		
	
	#calc populations fitness
	def calc_fitness(self):
		for indiviudal in self.populations:
			indiviudal.fitness = indiviudal.calc_fitness()

		#sort in decreasing order of fitness
		self.populations.sort(reverse= True, key=lambda x: x.fitness)

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

	def print_sol(self):
		print(len(self.trucks))
		for truck in self.best_sol.trucks:
			print(len(truck.solRoute))
			for node in truck.solRoute:
				print(node.ID, end = " ")
			print()
		
	def export_sol(self, file):
		with open(file, 'w') as f:
			f.write(f'{len(self.trucks)}\n')

			for truck in self.best_sol.trucks:
				f.write(f'{len(truck.solRoute)}\n')

				for node in truck.solRoute:
					f.write(f'{node.ID} ')
				
				f.write("\n")
		
		

def main():
	try:
		trucks, packages = import_data('2/test.txt')
	except:
		trucks, packages = import_data('test.txt')

	sol = GA(trucks, packages, 100, 100, 0.1)

	sol.solve()

	sol.print_sol()
	try:
		sol.export_sol('2/output.txt')
	except:
		sol.export_sol('output.txt')


if __name__ == "__main__":
	main()