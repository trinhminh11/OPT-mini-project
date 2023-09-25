import random
class Node:
	def __init__(self):
		pass
	def Order_cross_over(self, other):
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
	
	def Partially_mapped_cross_over(self, other):
		mom_chromosome = self.chromosome
		dad_chromosome = other.chromosome


		a = random.randint(1, self.n-1)
		b = random.randint(1, self.n-1)

		if a > b:
			a, b = b, a

		a = 3
		b = 7

		
		middle_chromosome1: list = mom_chromosome[a:b]
		middle_chromosome2: list = dad_chromosome[a:b]


		mapped = {middle_chromosome1[i]: middle_chromosome2[i] for i in range(len(middle_chromosome1))}


		for i in range(len(dad_chromosome[:a])):
			while dad_chromosome[i] in middle_chromosome1:
				dad_chromosome[i] = mapped[dad_chromosome[i]]


		for i in range(len(dad_chromosome[b:])):
			while dad_chromosome[i+b] in middle_chromosome1:
				dad_chromosome[i+b] = mapped[dad_chromosome[i+b]]


		child_chromosome = dad_chromosome[:a] + middle_chromosome1 + dad_chromosome[b:]

		return child_chromosome


	def Cycle_crossover(self, other):
		mom_chromosome: list = self.chromosome
		dad_chromosome: list = other.chromosome

		index = 0
		child_chromosome = [-1 for _ in range(self.n)]

		while child_chromosome.count(-1) != 0:

			gene = mom_chromosome[index]
			if gene not in child_chromosome:
				child_chromosome[index] = gene
			else:
				for i in range(len(child_chromosome)):
					if child_chromosome[i] == -1:
						child_chromosome[i] = dad_chromosome[i]
				
				break

			index = dad_chromosome.index(gene)


		return child_chromosome


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
			

for i in range(100):
	mom = Node()

	mom.chromosome = [1,2,3,4,5,6,7,8,9]
	random.shuffle(mom.chromosome)
	# print(mom.chromosome)
	mom.n = len(mom.chromosome)
	dad = Node()
	dad.chromosome = [4,1,2,8,7,6,9,3,5]
	random.shuffle(dad.chromosome)
	# print(dad.chromosome)

	child = mom.ERX(dad)

	child.sort()

	if child != [1,2,3,4,5,6,7,8,9]:
		print("error")