
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
	
	def check_valid(self):
		for task in self.prev:
			if task.depth == 0:
				self.remove_loop_branch()
		
		for task in self.next:
			task.check_valid()
	
	def remove_loop_branch(self):
		for task in self.prev:
			try:
				task.next.remove(self)
			except:
				pass

		for task in self.next:
			task.remove_loop_branch()

	
	# print for debug
	def __str__(self):
		return f'Task {self.ID}, depth = {self.depth}, size = {self.size}'

class Worker:
	def __init__(self, ID):
		self.ID = ID
		self.start = 0
		self.cost_tasks = []

		# dictinary with key = Task that this worker work on, value = Time Window to do this Task
		self.works = {}

		# work_flow of the worker
		self.works_flow = [[0, self.start]]
	
	def calc_work_flow(self):
		self.works_flow = [[0, self.start]] + list(self.works.values())
		self.works_flow.sort()
	


def import_data():
	N, Q = map(int, input().split())
	tasks = [Task(i+1) for i in range(N)]
	for _ in range(Q):
		i, j = map(int, input().split())

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
	
	for task in tasks:
		if task.depth == 1:
			task.check_valid()

	for task in tasks:
		if task.depth == 1:
			task.calc_depth()
	
	d = list(map(int, input().split()))

	#task duration
	for i in range(N):
		tasks[i].duration = d[i]
	
	M = int(input())
	workers = [Worker(i+1) for i in range(M)]

	s = list(map(int, input().split()))

	if len(s) == M+1:
		*s, K = s
	else:
		K = int(input())
	
	for i in range(M):
		workers[i].start = s[i]
		workers[i].works_flow = [[0, s[i]]]
		workers[i].cost_tasks = [-1 for _ in range(N)]
	

	for _ in range(K):
		i, j, c = map(int, input().split())

		workers[j-1].cost_tasks[i-1] = c

	return tasks, workers


'''
Heuristic:
Step 1:
	create a Tree, each Node is a Task
	Tree Depth is based on Q(i, j)
	if Task j can only be started to execute after the completion of task i -> task i is parent of task j and task j is child of task i
Step 2:
	loop through each task, sort workers based on workflow[-1][-1] is start free time of that worker
	loop through each worker, 
	if this task depth is 1, meaning this task does not depend on any task, add the worker has minimum workflow[-1][-1] that can work on this task
	else, calc timeDone of all task.prev (all tasks that this task depends on) and get the max timeDone
		if we have a worker's workflow[-1][-1] less than max timeDone and can work on this task, get the worker that has the minimum cost
		else, add the worker that has the minimum workflow[-1][-1] that can work on this task
'''

# Solver class
class Solver:
	def __init__(self, tasks, workers):
		self.tasks = tasks
		self.workers = workers
	
	# calc size for each task
	def calc_size(self):
		self.tasks.sort(key=lambda x: x.depth)

		for task in self.tasks[::-1]:            
			for t in task.prev:
				t.size += task.size
	
	# main solve function
	def solve(self):
		self.calc_size()
		self.tasks.sort(key= lambda x: [x.depth, -x.size, len(x.next)])

		# for task in self.tasks:
		# 	print(task.ID, task.depth)

		for task in self.tasks:
			if task.depth == 0:
				continue

			self.workers.sort(key= lambda x: [x.works_flow[-1][-1], x.cost_tasks[task.ID-1]])
			
			# if depth of task is 1, just add the worker has minimum works_flow[-1][-1] that can work on this task
			if task.depth == 1:
				for worker in self.workers:
					if worker.cost_tasks[task.ID-1] != -1:
						worker.works[task] = [worker.works_flow[-1][-1], worker.works_flow[-1][-1] + task.duration]
						task.timeDone = worker.works_flow[-1][-1] + task.duration
						worker.calc_work_flow()
						break

			elif len(task.prev) == 0:
				continue
			else:
				# calc max time of all task.prev
				max_time = -1
				for t in task.prev:
					# if task.ID == 638 and t.ID == 127:
					# 	print(t.timeDone, t.depth)

					if t.timeDone > max_time:
						max_time = t.timeDone
					
				best_cost = float('inf')

				best_worker = self.workers[0]

				for worker in self.workers:
					if worker.works_flow[-1][-1] <= max_time:
						if worker.cost_tasks[task.ID-1] != -1:
							if worker.cost_tasks[task.ID-1] < best_cost:
								best_worker = worker
								best_cost = worker.cost_tasks[task.ID-1]
				
				# if we have worker can work on this task and works_flow[-1][-1] <= max_time
				if best_cost < float('inf'):
					best_worker.works[task] = [max_time, max_time + task.duration]
					task.timeDone = max_time + task.duration
					best_worker.calc_work_flow()
				
				# if all worker can work on this task have works_flow[-1][-1] > max_time
				else:
					for worker in self.workers:
						if worker.cost_tasks[task.ID-1] != -1:
							worker.works[task] = [worker.works_flow[-1][-1], worker.works_flow[-1][-1] + task.duration]
							task.timeDone = worker.works_flow[-1][-1] + task.duration
							worker.calc_work_flow()
							break
				
	def print_sol(self):
		total = 0
		ans = ""

		sol = [[] for _ in range(len(self.tasks))]

		for worker in self.workers:
			if len(worker.works_flow) > 1:
				for task, time_window in worker.works.items():
					sol[task.ID-1] = [task.ID, worker.ID, time_window[0]]
		
		for s in sol:
			if s:
				ans += f'{s[0]} {s[1]} {s[2]}\n'
				total += 1
		
		print(total)
		print(ans[:-1])
	


def main():
	tasks, workers = import_data()


	sol = Solver(tasks, workers)

	sol.solve()

	sol.print_sol()




if __name__ == "__main__":
	main()
