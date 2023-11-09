from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def import_data():
	"""Stores the data for the problem."""
	N, K = map(int, input().split())
	data = {}
	data['demand'] = [0] + list(map(int, input().split()))
	data["time_matrix"] = []

	for i in range(N+1):
		data["time_matrix"].append(list(map(int, input().split())))

	data["num_vehicles"] = K
	data["depot"] = 0
	return data

class Solver:
	def __init__(self):
		self.data = import_data()
	
	def solve(self):
		# Create the routing index manager.
		self.manager = pywrapcp.RoutingIndexManager(
			len(self.data["time_matrix"]), self.data["num_vehicles"], self.data["depot"]
		)

		# Create Routing Model.
		self.routing = pywrapcp.RoutingModel(self.manager)

		# Create and register a transit callback.
		def distance_callback(from_index, to_index):
			"""Returns the distance between the two nodes."""
			# Convert from routing variable Index to distance matrix NodeIndex.
			from_node = self.manager.IndexToNode(from_index)
			to_node = self.manager.IndexToNode(to_index)
			return self.data["time_matrix"][from_node][to_node] + self.data['demand'][to_node]

		transit_callback_index = self.routing.RegisterTransitCallback(distance_callback)

		# Define cost of each arc.
		self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

		# Add Distance constraint.
		dimension_name = "Time"
		max_time = sum([max(self.data['time_matrix'][i]) for i in range(len(self.data['time_matrix']))])
		self.routing.AddDimension(
			transit_callback_index,
			0,  # no slack	
			max_time,  # vehicle maximum travel distance
			True,  # start cumul to zero
			dimension_name,
		)
		time_dimension = self.routing.GetDimensionOrDie(dimension_name)
		time_dimension.SetGlobalSpanCostCoefficient(100)

		# Setting first solution heuristic.
		search_parameters = pywrapcp.DefaultRoutingSearchParameters()
		search_parameters.first_solution_strategy = (
			routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
		)

		# Solve the problem.
		self.solution = self.routing.SolveWithParameters(search_parameters)



	def print_sol(self):
		print(self.data['num_vehicles'])
		for vehicle_id in range(self.data["num_vehicles"]):
			index = self.routing.Start(vehicle_id)
			route_distance = 0
			plan_output = ""
			count = 0
			while not self.routing.IsEnd(index):
				count += 1
				plan_output += f"{self.manager.IndexToNode(index)} "
				previous_index = index
				index = self.solution.Value(self.routing.NextVar(index))
				route_distance += self.routing.GetArcCostForVehicle(
					previous_index, index, vehicle_id
				)
			plan_output += f"{self.manager.IndexToNode(index)}"
			print(count+1)
			print(plan_output)


def main():
	sol = Solver()

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()