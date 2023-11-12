class Truck:
	def __init__(self, ID, lower, upper):
		self.ID = ID 
		self.lower = lower
		self.upper = upper
		self.load = 0
		self.packages = []


class Package:
	def __init__(self, ID, capacity, cost):
		self.ID = ID
		self.capacity = capacity
		self.cost = cost
		self.truck = False
		self.visited = False


def import_data():
	trucks = []
	packages = []
	N, K = map(int, input().split())
	for i in range(N):
		d, c = map(int, input().split())
		packages.append(Package(i+1, d, c))
	
	for i in range(K):
		c1, c2 = map(int, input().split())
		trucks.append(Truck(i+1, c1, c2))

	return packages, trucks;


class Solver:
	def __init__(self, packages, trucks):
		self.packages = packages
		self.N = len(self.packages)
		self.trucks = trucks
		self.K = len(self.trucks)
	
	def solve(self):
		for _ in range(self.N):
			best_pack = None
			max_cost = -1
			for package in self.packages:
				if package.visited:
					continue
				if package.cost > max_cost:
					max_cost = package.cost
					best_pack = package
			
			best_pack.visited = True

			best_truck = False
			min_dist = float('inf')

			for truck in self.trucks:
				if (0 <= truck.upper - (truck.load + best_pack.capacity) and truck.upper - (truck.load + best_pack.capacity) <= min_dist):
					min_dist = truck.upper - (truck.load + best_pack.capacity)
					best_truck = truck
			
			if best_truck:
				best_pack.truck = best_truck
				best_truck.load += best_pack.capacity
				best_truck.packages.append(best_pack)

		for truck in self.trucks:
			if (truck.lower <= truck.load and truck.load <= truck.upper):
				continue

			for package in truck.packages:
				package.truck = False
			
			truck.packages = []

	def print_sol(self):
		num_serve = 0
		ans = ""

		for package in self.packages:
			if package.truck:
				num_serve += 1
				ans += f'{package.ID} {package.truck.ID}\n'

		print(num_serve)
		print(ans)


def main():
	sol = Solver(*import_data())

	sol.solve()

	sol.print_sol()

if __name__ == "__main__":
	main()
