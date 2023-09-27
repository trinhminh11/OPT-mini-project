
# Passenget class represent a passenger have pick up ID and drop off ID
class Passenger:
	def __init__(self, ID, N):
		self.ID = ID

		self.pickup_ID = ID
		self.dropoff_ID = ID + N


class Truck:
	def __init__(self, Time_matrix, capacity, N):
		# solution Route is a sequence of Node, start and end = 0
		self.solRoute: list = [0, 0]    

		self.Time_matrix: list[list] = Time_matrix
		self.capacity = capacity

		self.N = N

	
	# check capacity constraint
	def check_constraint(self, Route: list):
		current_capacity = 0

		for node in Route[1:-1]:

			# if node is pickup
			if node <= self.N:
				current_capacity += 1
			# if node is drop off
			else:
				current_capacity -= 1
			
			if current_capacity > self.capacity:
				return False
		
		return True


	# calc run time of the Route
	def calc_runtime(self, Route: list):
		current_time = 0

		for i in range(len(Route)-1):
			current_time += self.Time_matrix[Route[i]][Route[i+1]]
		
		return current_time
	
	# find best index to insert a passenger to route
	def Insert(self, passenger: Passenger):
		temp_Route: list = self.solRoute.copy()
		best_Route: list = self.solRoute.copy()
		best_time = float('inf')

		for i in range(1, len(temp_Route)):

			# insert pickup to temp_Route
			temp_Route.insert(i, passenger.pickup_ID)
			
			# check capacity constraint
			if self.check_constraint(temp_Route):

				# insert drop off to temp_Route
				for j in range(i+1, len(temp_Route)):
					temp_Route.insert(j, passenger.dropoff_ID)
					time = self.calc_runtime(temp_Route)

					if time < best_time:
						best_time = time
						best_Route = temp_Route.copy()
					
					# reset temp Route
					temp_Route = self.solRoute.copy()
					temp_Route.insert(i, passenger.pickup_ID)

			# reset temp Route
			temp_Route = self.solRoute.copy()

		# if we update best time, meaning that we have a better Route, update solution Route
		if best_time != float('inf'):
			self.solRoute = best_Route.copy()
	
#import data from file
def import_data(file):
	#list contains Nodes object, Nodes[0] represent starting location
	Time_matrix: list[list[int]] = []
	passengers: list[Passenger] = []
	
	with open(file, 'r') as f:

		#number of Passenger, k
		N, k = map(int, f.readline().split())

		for i in range(N):
			passengers.append(Passenger(i+1, N))

		
		#get time matrix info
		for i in range(N*2 + 1):
			Time_matrix.append(list(map(int, f.readline().split())))

		truck = Truck(Time_matrix, k, N)
		

	# return Nodes and Time matrix
	return truck, passengers