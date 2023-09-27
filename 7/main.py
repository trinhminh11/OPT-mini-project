from CONSTANT import import_data, Truck, Passenger

class Solver:
	def __init__(self, truck: Truck, passengers: list[Passenger]):
		self.truck = truck
		self.passengers = passengers
	
	def solve(self):
		for passenger in self.passengers:
			self.truck.Insert(passenger)
	
	def print_sol(self):
		print(len(self.passengers))
		for Node in self.truck.solRoute[1:-1]:
			print(Node, end = " ")
		

	
	def export_sol(self, file):
		with open(file, 'w') as f:
			f.write(str(len(self.passengers)) + "\n")

			for Node in self.truck.solRoute[1:-1]:
				f.write(str(Node) + " ")

def main():
	try:
		truck, passengers = import_data('7/test.txt')
	except:
		truck, passengers = import_data('test.txt')
	
	sol = Solver(truck, passengers)

	sol.solve()

	sol.print_sol()

	try:
		sol.export_sol("7/output.txt")
	except:
		sol.export_sol("output.txt")

if __name__ == "__main__":
	main()