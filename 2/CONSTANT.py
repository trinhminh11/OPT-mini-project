random_seed = 11042004

# Process represent a Pick up or Delivery state of Package
class Process:
	def __init__(self, pID, ID, capacity, is_Pick):
		self.pID = pID
		self.ID = ID
		self.capacity = capacity
		self.is_Pick = is_Pick
	
	# print for debug
	def __str__(self):
		if self.is_Pick:
			return f'Pickup {self.pID} at {self.ID}, capacity = {self.capacity}'
		else:
			return f'Dropoff {self.pID} at {self.ID}, capacity = {self.capacity}'

# Package represent both Human and Request, if capacity == None => Human, else Request, each package contain 2 Process Pickup and Dropof
class Package:
	def __init__(self, ID, pID, dID, capacity):
		self.ID = ID
		self.pID = pID
		self.dID = dID
		self.capacity = capacity

		self.Pickup = Process(ID, pID, capacity, True)
		self.Dropoff = Process(ID, dID, capacity, False)
	

# Truck represent a Truck, have ID and capacity
class Truck:
	def __init__(self, ID, capacity, distance_matrix):
		self.ID = ID
		self.capacity = capacity
		self.distance_matrix = distance_matrix

		# list of packages that this truck delivery
		self.packages: list[Package] = []

		# Route of the Truck, list of Processes
		self.solRoute: list[Process] = [Process(0, 0, 0, True), Process(0, 0, 0, False)]
		
		# Time Done of the last Process is runtime off the Truck
		self.solRoute[-1].timeDone = 0
	
	# check capacity constraint and calc time
	def check_constraint(self, Route: list[Process]):
		current_capacity = 0
		current_time = 0

		for i in range(1, len(Route)):

			current_time += self.distance_matrix[Route[i-1].ID][Route[i].ID]

			# if this Process is human, do nothing
			if Route[i].capacity == None:
				continue
			# if this Process is Pickup, add Process capacity to current capacity
			if Route[i].is_Pick:
				current_capacity += Route[i].capacity
			else:
				current_capacity -= Route[i].capacity
			
			# if capacity greater than capacity of truck, return False
			if current_capacity > self.capacity:
				return False
		# timeDone of last Process is run time of Truck
		Route[-1].timeDone = current_time
		return True
	
	# insert package to truck
	def Insert(self, package: Package):
		
		# temp Route, best Route is the copy of solRoute
		temp_Route = self.solRoute.copy()
		best_Route = self.solRoute.copy()
		best_time = float('inf')

		# run through temp_Route except first Process and last Process
		for i in range(1, len(temp_Route)):
			# if 2 consecutive Process is human, pass, do nothing
			if temp_Route[i-1].capacity == None and temp_Route[i].capacity == None and temp_Route[i-1].pID == temp_Route[i].pID:
				continue
			
			# insert package'Pickup to index i
			temp_Route.insert(i, package.Pickup)

			# check constraint after insert
			if self.check_constraint(temp_Route):

				# if package is human
				if package.capacity == None:
					# insert packge's Dropoff right in next index
					temp_Route.insert(i+1, package.Dropoff)

					if self.check_constraint(temp_Route):
						temp_time = temp_Route[-1].timeDone
						# if new time better than best_time, update best Route, best time
						if temp_time < best_time:
							best_time = temp_time
							best_Route = temp_Route.copy()
				
				else:
					# loop through temp_Route from index i+1
					for j in range(i+1, len(temp_Route)):
						# if 2 consecutive Process is human, pass, do nothing
						if temp_Route[j-1].capacity == None and temp_Route[j].capacity == None and temp_Route[j-1].pID == temp_Route[j].pID:
							continue
						
						# insert package's Dropoff to index j
						temp_Route.insert(j, package.Dropoff)

						if self.check_constraint(temp_Route):
							temp_time = temp_Route[-1].timeDone

							# if new time better than best_time, update best Route, best time
							if temp_time < best_time:
								best_time = temp_time
								best_Route = temp_Route.copy()
							
							# reset temp Route
							temp_Route = self.solRoute.copy()
							temp_Route.insert(i, package.Pickup)
			
			#reset temp Route
			temp_Route = self.solRoute.copy()
		
		# assume that Insert will always success, update solRoute to bestRoute
		if best_time < float('inf'):
			self.solRoute = best_Route.copy()
			self.solRoute[-1].timeDone = best_time
			return True
		
		# if not, print for debug
		else:
			print("here")
			exit()

def import_data(file):
	distance_matrix = []
	trucks = []
	packages = []
	with open(file, 'r') as f:
		N, M, K = map(int, f.readline().split())
		q = list(map(int, f.readline().split()))
		Q = list(map(int, f.readline().split()))

		for i in range(2*N+2*M+1):
			distance_matrix.append(list(map(int, f.readline().split())))

		for i in range(K):
			trucks.append(Truck(i+1, Q[i], distance_matrix))
		
		for i in range(1, N + 1):
			if i <= N:
				packages.append(Package(i, i, i+N+M, None))
		for i in range(1, M + 1):
				packages.append(Package(i+N, i+N, i+2*N+M, q[i-1]))
		
	return trucks, packages	