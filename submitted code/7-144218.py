def import_data():
	N, K = map(int, input().split())
	distance_matrix = []
 
	for i in range(2*N+1):
		distance_matrix.append(list(map(int, input().split())))
   
	return N, K, distance_matrix

class Solver:
	def __init__(self, N, K, distance_matrix):
		self.N = N
		self.K = K
		self.Num_Nodes = 2*N + 1

		self.distance_matrix = distance_matrix
		self.visited = [False for _ in range(self.Num_Nodes)]
		self.demands = [1 if 1 <= i and i <= N else -1 for i in range(self.Num_Nodes)]

	def solve(self):
		self.ans = []

		current_node = 0
		capacity = 0

		for _ in range(self.Num_Nodes-1):
			min_dist = float('inf')
			best_node = -1

			for node in range(1, self.Num_Nodes):
				if self.visited[node] or capacity + self.demands[node] > self.K:
					continue

				if node > self.N:
					if not self.visited[node-self.N]:
						continue

				if self.distance_matrix[current_node][node] < min_dist:
					min_dist = self.distance_matrix[current_node][node]
					best_node = node

			self.ans.append(best_node)
			self.visited[best_node] = True
			capacity += self.demands[best_node]

			current_node = best_node
	
	def print_sol(self):
		print(self.N)
		print(*self.ans)

def main():
	N, K, distance_matrix = import_data()

	sol = Solver(N, K, distance_matrix)

	sol.solve()

	sol.print_sol()
  

if __name__ == "__main__":
	main()