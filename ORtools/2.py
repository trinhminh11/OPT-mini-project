"""Simple Pickup Delivery Problem (PDP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def import_data():
	"""Stores the data for the problem."""
	data = {}

	N, M, K = map(int, input().split())
	q = list(map(int, input().split()))
	data['Num_passengers'] = N
	data['Num_packages'] = M
	data["vehicle_capacities"] = list(map(int, input().split()))
	data["distance_matrix"] = []
	data["pickups_deliveries"] = []
	data['demands'] = [0]

	for i in range(2*N+2*M+1):
		data["distance_matrix"].append(list(map(int, input().split())))
		if 1 <= i <= N:
			data['pickups_deliveries'].append([i, i+N+M])
			data['demands'].append(0)

		if N+1 <= i <= N+M:
			data['pickups_deliveries'].append([i, i+N+M])
			data['demands'].append(q[i-N-1])
		
		if N+M+1 <= i <= 2*N+M:
			data['demands'].append(0)
		
		if 2*N+M+1 <= i <= 2*N + 2*M:
			data['demands'].append(-q[i-2*N-M-1])

	data["num_vehicles"] = K
	data["depot"] = 0
	return data

class Solver:
	def __init__(self, data):
		self.data = data
	
	def solve(self):
		# Create the routing index manager.
		self.manager = pywrapcp.RoutingIndexManager(
			len(self.data["distance_matrix"]), self.data["num_vehicles"], self.data["depot"]
		)

		# Create Routing Model.
		self.routing = pywrapcp.RoutingModel(self.manager)


		# Define cost of each arc.
		def distance_callback(from_index, to_index):
			"""Returns the manhattan distance between the two nodes."""
			# Convert from routing variable Index to distance matrix NodeIndex.
			from_node = self.manager.IndexToNode(from_index)
			to_node = self.manager.IndexToNode(to_index)
			return self.data["distance_matrix"][from_node][to_node]

		transit_callback_index = self.routing.RegisterTransitCallback(distance_callback)
		self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

		# Add Distance constraint.
		dimension_name = "Distance"
		max_dist = sum([max(self.data['distance_matrix'][i]) for i in range(len(self.data['distance_matrix']))])
		self.routing.AddDimension(
			transit_callback_index,
			0,  # no slack
			max_dist,  # vehicle maximum travel distance
			True,  # start cumul to zero
			dimension_name,
		)
		distance_dimension = self.routing.GetDimensionOrDie(dimension_name)
		distance_dimension.SetGlobalSpanCostCoefficient(100)

		def demand_callback(from_index):
			"""Returns the demand of the node."""
			# Convert from routing variable Index to demands NodeIndex.
			from_node = self.manager.IndexToNode(from_index)
			return self.data["demands"][from_node]

		demand_callback_index = self.routing.RegisterUnaryTransitCallback(demand_callback)
		self.routing.AddDimensionWithVehicleCapacity(
			demand_callback_index,
			0,  # null capacity slack
			self.data["vehicle_capacities"],  # vehicle maximum capacities
			True,  # start cumul to zero
			"Capacity",
		)

		# Define Transportation Requests.
		for request in self.data["pickups_deliveries"]:
			pickup_index = self.manager.NodeToIndex(request[0])
			delivery_index = self.manager.NodeToIndex(request[1])
			self.routing.AddPickupAndDelivery(pickup_index, delivery_index)
			self.routing.solver().Add(
				self.routing.VehicleVar(pickup_index) == self.routing.VehicleVar(delivery_index)
			)
			self.routing.solver().Add(
				distance_dimension.CumulVar(pickup_index)
				<= distance_dimension.CumulVar(delivery_index)
			)
		

		for i in range(1, self.data['Num_passengers']+1):
			pickup_index = self.manager.NodeToIndex(i)
			dropoff_index = self.manager.NodeToIndex(i+self.data['Num_passengers'] + self.data['Num_packages'])

			self.routing.solver().Add(
				distance_dimension.CumulVar(pickup_index) + self.data['distance_matrix'][i][i+self.data['Num_passengers'] + self.data['Num_packages']]
				== distance_dimension.CumulVar(dropoff_index)
			)


		# Setting first solution heuristic.
		search_parameters = pywrapcp.DefaultRoutingSearchParameters()
		search_parameters.first_solution_strategy = (
			routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
		)

		# Solve the problem.
		self.solution = self.routing.SolveWithParameters(search_parameters)

	
	def print_sol(self):
		"""Prints solution on console."""
		print(self.data["num_vehicles"])
		for vehicle_id in range(self.data["num_vehicles"]):
			index = self.routing.Start(vehicle_id)
			plan_output = f""
			count = 0
			while not self.routing.IsEnd(index):
				count += 1
				plan_output += f"{self.manager.IndexToNode(index)} "
				index = self.solution.Value(self.routing.NextVar(index))
			plan_output += f"{self.manager.IndexToNode(index)}"
			print(count+1)
			print(plan_output)


def main():
	data = import_data()

	sol = Solver(data)

	sol.solve()

	sol.print_sol()
	


if __name__ == "__main__":
	main()