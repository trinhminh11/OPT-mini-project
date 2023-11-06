class Node:
	def __init__(self, ID, e, l, d):
		self.ID = ID
		self.e = e
		self.l = l
		self.d = d
		self.time_done = 0

def import_data():
	N = int(input())
	nodes = [Node(0, 0, float('inf'), 0)]
	time_matrix = []
	for i in range(N):
		e, l, d = map(int, input().split())
		nodes.append(Node(i+1, e, l, d))
	
	for i in range(N+1):
		time_matrix.append(list(map(int, input().split())))

	return nodes, time_matrix

class Solver:
	def __init__(self, nodes, time_matrix):
		self.N = len(nodes)-1
		self.nodes = nodes
		self.time_matrix = time_matrix
		self.route = [nodes[0]]
	
	def calc_runtime(self):
		current_time = 0
		for i in range(1, len(self.route)):
			current_time += self.time_matrix[self.route[i-1].ID][self.route[i].ID]
			
			if current_time <= self.route[i].l:
				current_time = max(current_time, self.route[i].e) + self.route[i].d
			else:
				print("WTF??")
				exit()
			
			self.route[i].time_done = current_time
		

	def Insert(self, node):
		best_time = float('inf')
		best_pos = -1


		for i in range(1, len(self.route) + 1):
			current_time = self.route[i-1].time_done + self.time_matrix[self.route[i-1].ID][node.ID]
			
			if current_time < node.e:
				current_time = node.e
			
			if current_time > node.l:
				break 
			
			current_time += node.d


			
			for j in range(i, len(self.route)):
				if j == i:

					current_time += self.time_matrix[node.ID][self.route[j].ID]
				else:
					current_time += self.time_matrix[self.route[j-1].ID][self.route[j].ID]
				if current_time < self.route[j].e:
					current_time = self.route[j].e
				if current_time > self.route[j].l:
					break

				current_time += self.route[j].d
			
			else:
				run_time = current_time + self.time_matrix[self.route[-1].ID][0]
				if run_time < best_time:
					best_time = run_time
					best_pos = i

		if best_pos != -1:
			self.route.insert(best_pos, node)
			self.calc_runtime()

	def solve(self):
		for i in range(1, self.N+1):
			self.Insert(self.nodes[i])
	
	def print_sol(self):
		print(len(self.route)-1)

		for node in self.route[1:]:
			print(node.ID, end = " ")


def main():
	nodes, time_matrix = import_data()

	sol = Solver(nodes, time_matrix)

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()