"""Simple Pickup Delivery Problem (PDP)."""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def import_data():
	N, K = map(int, input().split())
	data = {}
	data["distance_matrix"] = []
	data["pickups_deliveries"] = []
	data['demands'] = [0]
	for i in range(2*N+1):
		data["distance_matrix"].append(list(map(int, input().split())))
		if 1 <= i and i <=N:
			data["pickups_deliveries"].append([i, i+N])
			data['demands'].append(1)
		
		if N < i:
			data['demands'].append(-1)
		
	data["num_vehicles"] = 1
	data['vehicle_capacities'] = [K]
	data["depot"] = 0
	return data

class Solver:
	def __init__(self):
		self.data = import_data()
	
	def solve(self):
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
		max_dist = sum([max(self.data['distance_matrix'][i]) for i in range(len(self.data['distance_matrix']))])
		dimension_name = "Distance"
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

		# Setting first solution heuristic.
		search_parameters = pywrapcp.DefaultRoutingSearchParameters()
		search_parameters.first_solution_strategy = (
			routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
		)

		# Solve the problem.
		self.solution = self.routing.SolveWithParameters(search_parameters)

	def print_sol(self):
		"""Prints solution on console."""
		total_distance = 0
		for vehicle_id in range(self.data["num_vehicles"]):
			index = self.routing.Start(vehicle_id)
			count = 0
			route = []
			while not self.routing.IsEnd(index):
				count += 1
				route.append(self.manager.IndexToNode(index))

				index = self.solution.Value(self.routing.NextVar(index))

			route.append(self.manager.IndexToNode(index))

			print((count-1)//2)
			print(*route[1:-1])



def main():
	sol = Solver()

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()