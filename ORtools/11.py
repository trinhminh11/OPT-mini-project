from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

#import data
def import_data():
	data = {}
	N, K = map(int, input().split())

	data['num_vehicles'] = K
	data['starts'] = [0 for _ in range(K)]
	data['ends'] = [N+1 for _ in range(K)]

	data['distance_matrix'] = []

	for i in range(N+1):
		data['distance_matrix'].append(list(map(int, input().split())) + [0])
	
	data['distance_matrix'].append([0 for _ in range(N+2)])
	
	return data



class Solver:
	def __init__(self, data):
		self.data = data
	
	def solve(self):
		# Create the routing index manager.
		self.manager = pywrapcp.RoutingIndexManager(len(self.data['distance_matrix']),
											self.data['num_vehicles'], self.data['starts'],
											self.data['ends'])

		# Create Routing Model.
		self.routing = pywrapcp.RoutingModel(self.manager)


		# Create and register a transit callback.
		def distance_callback(from_index, to_index):
			"""Returns the distance between the two nodes."""
			# Convert from routing variable Index to distance matrix NodeIndex.
			from_node = self.manager.IndexToNode(from_index)
			to_node = self.manager.IndexToNode(to_index)
			return self.data['distance_matrix'][from_node][to_node]

		transit_callback_index = self.routing.RegisterTransitCallback(distance_callback)

		# Define cost of each arc.
		self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

		# Add Distance constraint.
		max_dist = sum([max(self.data['distance_matrix'][i]) for i in range(len(self.data['distance_matrix']))])
		dimension_name = 'Distance'
		self.routing.AddDimension(
			transit_callback_index,
			0,  # no slack
			max_dist,  # vehicle maximum travel distance
			True,  # start cumul to zero
			dimension_name)
		distance_dimension = self.routing.GetDimensionOrDie(dimension_name)
		distance_dimension.SetGlobalSpanCostCoefficient(100)

		# Setting first solution heuristic.
		search_parameters = pywrapcp.DefaultRoutingSearchParameters()
		search_parameters.first_solution_strategy = (
			routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

		# Solve the problem.
		self.solution = self.routing.SolveWithParameters(search_parameters)

	
	def print_sol(self):
		"""Prints solution on console."""
		print(self.data['num_vehicles'])
		for vehicle_id in range(self.data['num_vehicles']):
			index = self.routing.Start(vehicle_id)
			
			count = 0
			plan_output = ''
			while not self.routing.IsEnd(index):
				plan_output += f'{self.manager.IndexToNode(index)} '
				index = self.solution.Value(self.routing.NextVar(index))
				count += 1
			
			print(count)
			print(plan_output)

def main():
	data = import_data()
	
	sol = Solver(data)

	sol.solve()

	sol.print_sol()


if __name__ == '__main__':
	main()