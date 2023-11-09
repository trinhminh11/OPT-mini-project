"""Vehicles Routing Problem (VRP) with Time Windows."""
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

#Nodes object represent ID of Node, earliest and latest time to serve and time to delivery package
class Node:
	def __init__(self, ID, e, l, d):
		self.ID = ID
		self.e = e
		self.l = l
		self.d = d

		#time after delivery package
		self.timeDone = 0
	
	#printing for debug
	def __str__(self):
		return f'ID: {self.ID}, e: {self.e}, l: {self.l}, d: {self.d}, timeDone: {self.timeDone}.'
	
#import data from file
def import_data():
	#list contains Nodes object, Nodes[0] represent starting location
	Nodes = [Node(0, 0, 28800, 0)]
	Time_matrix = []

	#number of Node
	N = int(input())

	#get Node info
	for i in range(N):
		e, l, d = map(int, input().split())
		Nodes.append(Node(i+1, e, l, d))
	
	#get time matrix info
	for i in range(N+1):
		Time_matrix.append(list(map(int, input().split())))

    # return Nodes and Time matrix
	return Nodes, Time_matrix

def create_data_model(Nodes, Time_matrix):
	"""Stores the data for the problem."""
	data = {}
	data["time_matrix"] = Time_matrix
	data["time_windows"] = [(node.e, node.l) for node in Nodes]
	data['demands'] = [node.d for node in Nodes]
	data["depot"] = 0
	return data
	

class Solver:
	def __init__(self, Nodes, Time_matrix):
		self.data = create_data_model(Nodes, Time_matrix)
		self.vehicle_id = 0
	
	def solve(self):
		self.manager = pywrapcp.RoutingIndexManager(
			len(self.data["time_matrix"]), 1, self.data["depot"]
		)

		self.vehicle_id = 0

		# Create Routing Model.
		self.routing = pywrapcp.RoutingModel(self.manager)

		# Create and register a transit callback.
		def time_callback(from_index, to_index):
			"""Returns the travel time between the two nodes."""
			# Convert from routing variable Index to time matrix NodeIndex.
			from_node = self.manager.IndexToNode(from_index)
			to_node = self.manager.IndexToNode(to_index)
			return self.data["time_matrix"][from_node][to_node] + self.data['demands'][from_node]

		transit_callback_index = self.routing.RegisterTransitCallback(time_callback)

		# Define cost of each arc.
		self.routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

		# Add Time Windows constraint.
		time = "Time"
		self.routing.AddDimension(
			transit_callback_index,
			sum(self.data['demands']),# allow waiting time,
			sum([max(self.data['time_matrix'][i]) for i in range(len(self.data['time_matrix']))]),  # maximum time per vehicle
			False,  # Don't force start cumul to zero.
			time,
		)

		time_dimension = self.routing.GetDimensionOrDie(time)
		# Add time window constraints for each location except depot.
		for location_idx, time_window in enumerate(self.data["time_windows"]):
			if location_idx == self.data["depot"]:
				continue
			index = self.manager.NodeToIndex(location_idx)
			time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
		# Add time window constraints for each vehicle start node.
		depot_idx = self.data["depot"]
		
		index = self.routing.Start(self.vehicle_id)
		time_dimension.CumulVar(index).SetRange(
			self.data["time_windows"][depot_idx][0], self.data["time_windows"][depot_idx][1]
		)

		# Instantiate route start and end times to produce feasible times.
		self.routing.AddVariableMinimizedByFinalizer(
			time_dimension.CumulVar(self.routing.Start(self.vehicle_id))
		)
		self.routing.AddVariableMinimizedByFinalizer(time_dimension.CumulVar(self.routing.End(self.vehicle_id)))

		# Setting first solution heuristic.
		search_parameters = pywrapcp.DefaultRoutingSearchParameters()
		search_parameters.first_solution_strategy = (
			routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
		)

		# Solve the problem.
		self.solution = self.routing.SolveWithParameters(search_parameters)

			
	def print_sol(self):
		"""Prints solution on console."""

		index = self.routing.Start(self.vehicle_id)
		plan_output = ""
		count = 0
		while not self.routing.IsEnd(index):
			if index != 0:
				plan_output += f"{self.manager.IndexToNode(index)} "

			index = self.solution.Value(self.routing.NextVar(index))
			count += 1
		
		print(count-1)
		
		print(plan_output)
	


def main():
	Nodes, Time_matrix = import_data()
	
	sol = Solver(Nodes, Time_matrix)

	sol.solve()

	sol.print_sol()



if __name__ == "__main__":
	main()