#import data from file
def import_data():
	distance_matrix: list[list[int]] = []
	

	#number of Passenger, k
	N, K = map(int, input().split())

	Q = list(map(int, input().split()))
	
	#get time matrix info
	for i in range(N + 1):
		distance_matrix.append(list(map(int, input().split())))


	# return Nodes and Time matrix
	return N, K, Q, distance_matrix


class Solver:
	def __init__(self, N, K, Q, distance_matrix):
		self.N = N
		self.K = K
		self.Q = [0] + Q
		self.distance_matrix = distance_matrix
		
		self.visited = [False for i in range(N+1)]

		self.hub = 0
	
	def solve(self):
		ans = [-1 for _ in range(self.N+1)]
		ans[0] = self.hub
		self.total_dist = float('inf')
		self.current_dist = 0
		self.capacity = 0

		def bt(pos):
			if pos == self.N+1:
				if self.capacity >= self.K and self.current_dist + self.distance_matrix[ans[-1]][0] < self.total_dist:
					self.total_dist = self.current_dist + self.distance_matrix[ans[-1]][0]
				
				return
				
			

			for i in range(1, self.N+1):
				if self.visited[i]:
					continue
				ans[pos] = i
				self.visited[i] = True
				self.capacity += self.Q[i]
				self.current_dist += self.distance_matrix[ans[pos-1]][ans[pos]]
				if self.capacity >= self.K:
					if self.current_dist + self.distance_matrix[ans[pos]][0] < self.total_dist:
						self.total_dist = self.current_dist + self.distance_matrix[ans[pos]][0]

				

				if self.current_dist < self.total_dist:
					bt(pos+1)
				
				self.visited[i] = False
				self.capacity -= self.Q[i]
				self.current_dist -= self.distance_matrix[ans[pos-1]][ans[pos]]
		
		bt(1)
				
	
	def print_sol(self):
		# print(self.N)
		# print(*self.result[1:])
		print(self.total_dist)


def main():
	N, K, Q, distance_matrix = import_data()

	sol = Solver(N, K, Q, distance_matrix)

	sol.solve()
	
	sol.print_sol()
 
if __name__ == "__main__":
	main()
