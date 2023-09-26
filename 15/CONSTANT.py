random_seed = 11042004


# Class Pacakge represent a Package, contain ID, capacity and cost
class Package:
	def __init__(self, ID, capacity, cost):
		self.ID = ID
		self.capacity = capacity
		self.cost = cost

		# self.truck_used is Truck that delivery this package, initial is a dummy truck
		self.truck_used: Truck = Truck(0, 0, 0)
	
	# print for debug
	def __str__(self):
		return f'package: {self.ID}, capacity = {self.capacity}, cost = {self.cost}'

# class Truck represent a Truck, contain ID, lower bound, upper bound, current capacity and current cost of that truck
class Truck:
	def __init__(self, ID, lower_bound, upper_bound):
		self.ID = ID
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound
		self.capacity = 0
		self.cost = 0

		# self.pacakges is list of Package that this truck delivery
		self.packages: list[Package] = []
	
	
	# print for debug
	def __str__(self):
		return f'truck: {self.ID}, {self.lower_bound} - {self.upper_bound}, current_capacity = {self.capacity}, cost = {self.cost}'
	
		
# improt data
def import_data(file):
	packages = []
	trucks = []
	with open(file, 'r') as f:
		N, K = map(int, f.readline().split())

		for i in range(N):
			l, c = map(float, f.readline().split())
			packages.append(Package(i+1, l, c))
		
		for i in range(K):
			c1, c2 = map(float, f.readline().split())
			trucks.append(Truck(i+1, c1, c2))
	
	return packages, trucks
