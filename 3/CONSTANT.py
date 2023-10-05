
class Task:
	def __init__(self, ID):
		self.ID = ID
		self.depth = 0
		self.prev: list[Task] = []
		self.next: list[Task] = []
		self.duration = 0
		self.size = 1

		# TimeDone
		self.timeDone = -1
	
	# calc depth for all next tasks
	def calc_depth(self):
		for task in self.next:
			task.depth = max(task.prev, key= lambda x: x.depth).depth + 1

		for task in self.next:
			task.calc_depth()
	
	# print for debug
	def __str__(self):
		return f'Task {self.ID}, depth = {self.depth}, size = {self.size}'

class Worker:
	def __init__(self, ID):
		self.ID = ID
		self.start = 0
		self.cost_tasks: list = []

		# dictinary with key = Task that this worker work on, value = Time Window to do this Task
		self.works: dict[Task, list[int]] = {}

		# work_flow of the worker
		self.works_flow: list[list[int]] = [[0, self.start]]
	
	def calc_work_flow(self):
		self.works_flow = [[0, self.start]] + list(self.works.values())
		self.works_flow.sort()

	


def import_data(file):


	with open(file, 'r') as f:
		N, Q = map(int, f.readline().split())
		tasks = [Task(i+1) for i in range(N)]
		for _ in range(Q):
			i, j = map(int, f.readline().split())

			tasks[i-1].next.append(tasks[j-1])

			tasks[j-1].prev.append(tasks[i-1])
		
		
		# initial depth
		for i in range(N):
			if len(tasks[i].prev) == 0:
				tasks[i].depth = 1
		
		# calc all tasks depth
		for task in tasks:
			if task.depth == 1:
				task.calc_depth()
		
		d = list(map(int, f.readline().split()))

		#task duration
		for i in range(N):
			tasks[i].duration = d[i]
		
		M = int(f.readline())
		workers = [Worker(i+1) for i in range(M)]
		s = list(map(int, f.readline().split()))

		for i in range(M):
			workers[i].start = s[i]
			workers[i].works_flow = [[0, s[i]]]
			workers[i].cost_tasks = [-1 for _ in range(N)]
		
		K = int(f.readline())

		for _ in range(K):
			i, j, c = map(int, f.readline().split())

			workers[j-1].cost_tasks[i-1] = c
	
	return tasks, workers


