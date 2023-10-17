from CONSTANT import import_data, Task, Worker

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
	def __init__(self, tasks: list[Task], workers: list[Worker]):
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

		for task in self.tasks:
			self.workers.sort(key= lambda x: [x.works_flow[-1][-1], x.cost_tasks[task.ID-1]])
			
			# if depth of task is 1, just add the worker has minimum works_flow[-1][-1] that can work on this task
			if task.depth == 1:
				for worker in self.workers:
					if worker.cost_tasks[task.ID-1] != -1:
						worker.works[task] = [worker.works_flow[-1][-1], worker.works_flow[-1][-1] + task.duration]
						task.timeDone = worker.works_flow[-1][-1] + task.duration
						worker.calc_work_flow()
						break

			else:
				# calc max time of all task.prev
				max_time = -1
				for t in task.prev:
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
		print(ans)
	
	def export_sol(self, file):
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
		with open(file, 'w') as f:
			f.write(str(total) + "\n")
			f.write(ans)
			



def main(inp, out):
	tasks, workers = import_data(inp)

	sol = Solver(tasks, workers)

	sol.solve()

	sol.print_sol()

	sol.export_sol(out)



if __name__ == "__main__":
	inp = f'test.txt'
	out = f'output.txt'
	main(inp, out)