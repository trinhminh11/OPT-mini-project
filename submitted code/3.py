
class Task:
	def __init__(self, ID):
		self.ID = ID
		self.depth = 0
		self.num_prev = 0
		self.prev = []
		self.next = []
		self.duration = 0
		self.size = 1

		# TimeDone
		self.timeDone = -1
	
	# print for debug
	def __str__(self):
		return f'Task {self.ID}, depth = {self.depth}, size = {self.size}'

class Worker:
	def __init__(self, ID):
		self.ID = ID
		self.start = 0
		self.cost_tasks = []

		# dictinary with key = Task that this worker work on, value = Time Window to do this Task

		self.last_work = 0
	
	


def import_data():
	N, Q = map(int, input().split())
	tasks = [Task(i+1) for i in range(N)]
	for _ in range(Q):
		i, j = map(int, input().split())

		tasks[i-1].next.append(tasks[j-1])

		tasks[j-1].prev.append(tasks[i-1])

		tasks[j-1].num_prev += 1

		tasks[j-1].depth += 1

	
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
		workers[i].last_work = s[i]
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
	loop through each task, sort workers based on last_work is the last working time of that worker
	calc timeDone of all task.prev (all tasks that this task depends on) and get the max TimeDone
		loop through each worker, 
		add the worker have the maximum [max(last_work, max TimeDone), cost] to work on this task
'''

# Solver class
class Solver:
	def __init__(self, tasks, workers):
		self._tasks = tasks
		self.tasks = []
		self.workers = workers
	
	
	def topo_task(self):
		search_task = [task for task in self._tasks if task.depth == 0]

		while search_task:
			current_task = search_task.pop(0)
			self.tasks.append(current_task)

			for task in current_task.next:
				task.num_prev -= 1
				if task.num_prev == 0:
					search_task.append(task)

	
	# main solve function
	def solve(self):
		self.topo_task()

		self.result = []

		for task in self.tasks:
			max_time = -1
			for t in task.prev:
				if t.timeDone > max_time:
					max_time = t.timeDone

			self.workers.sort(key= lambda x: [max(x.last_work, max_time), x.cost_tasks[task.ID-1], x.ID])

			for worker in self.workers:
				if worker.cost_tasks[task.ID-1] != -1:
					task.timeDone = max(worker.last_work, max_time) + task.duration
					worker.last_work = task.timeDone
					self.result.append([task.ID, worker.ID, task.timeDone - task.duration])
					break
		
		self.result.sort()
				
	def print_sol(self):
		print(len(self.result))

		for result in self.result:
			print(*result)
	


def main():
	tasks, workers = import_data()


	sol = Solver(tasks, workers)

	sol.solve()

	sol.print_sol()



if __name__ == "__main__":
	main()
