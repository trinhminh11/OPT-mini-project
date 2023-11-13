"""Solves a flexible jobshop problems with the CP-SAT solver.

A jobshop is a standard scheduling problem when you must sequence a
series of task_types on a set of machines. Each job contains one task_type per
machine. The order of execution and the length of each job on each
machine is task_type dependent.

"""


from ortools.sat.python import cp_model

# Teacher class represent a Teacher, contain ID and all subjects of that teacher
class Teacher:
	def __init__(self, ID, subjects: list[int]):
		self.ID = ID
		self.subjects = subjects

		# dictionary with key = slot, value = True if this teacher busy on that slot and False if this teacher free
		self.used = [False for i in range(1, 61)]
	
	def reset(self):
		self.used = [False for i in range(1, 61)]
	
	# print for debug
	def __str__(self):
		ans = f'Teacher: {self.ID}, subjects = ['

		for subject in self.subjects[:-1]:
			ans += f'{subject}, '
		
		ans += f'{self.subjects[-1]}]'

		return ans

# Class class represent a Class, contain ID and all subjects that this class have to study
class Class:
	def __init__(self, ID, subjects: list[int]):
		self.ID = ID
		self.subjects = subjects

		# Possible teacher can teach this Class
		# dict with key = subject, value = list of teacher can teach this subject
		self.teachers: dict[int, list[Teacher]] = {subject: [] for subject in self.subjects}

		# dict with key = subject, value = [start time slot that teacher assign to this class, teacher]
		self.sol: dict[int, list[int]] = {s: [] for s in subjects}

		self.used = [False for i in range(1, 61)]


	# print for debug
	def __str__(self):
		ans = f'Class: {self.ID}, subjects = ['

		for subject in self.subjects[:-1]:
			ans += f'{subject}, '
		
		ans += f'{self.subjects[-1]}]'

		return ans

def find_possible_teachers(classes: list[Class], teachers: list[Teacher]):
	for c in classes:
		for subject in c.subjects:
			for teacher in teachers:
				if subject in teacher.subjects:
					c.teachers[subject].append(teacher)
		


def import_data():
	classes: list[Class] = []
	teachers: list[Teacher] = []

	
	T, N, M = map(int, input().split())

	for i in range(N):
		temp = list(map(int, input().split()))
		temp.pop()


		classes.append(Class(i+1, temp))
	
	for i in range(T):
		temp = list(map(int, input().split()))
		temp.pop()

		teachers.append(Teacher(i+1, temp))
	
	temp = list(map(int, input().split()))
	
	#dictionary key = subject ID, value = preiods
	subjects = {i+1: temp[i] for i in range(M)}
	find_possible_teachers(classes, teachers)


	return classes, teachers, subjects



class Solver:
	def __init__(self, classes, teachers, subjects):
		self.classes = classes
		self.teachers = teachers
		self.subjects = subjects
		self.jobs = self.encode_data()
	
	# encode data
	def encode_data(self):
		jobs = [
			[
				[
					(self.subjects[subject], teacher.ID-1) for teacher in c.teachers[subject]
				] if c.teachers[subject] else [(0, -1)] for subject in c.subjects
			] for c in self.classes
		]
		
		
		return jobs
		

	def solve(self):
		num_jobs = len(self.jobs)
		all_jobs = range(num_jobs)

		num_machines = len(self.teachers)
		all_machines = range(num_machines)

		# Model the flexible jobshop problem.
		model = cp_model.CpModel()

		# upper bound of makespan
		horizon = 0
		for job in self.jobs:
			for task in job:
				max_task_duration = 0
				for alternative in task:
					max_task_duration = max(max_task_duration, alternative[0])
				horizon += max_task_duration


		# Global storage of variables.
		intervals_per_resources = {}
		self.starts = {}  # indexed by (job_id, task_id).
		self.presences = {}  # indexed by (job_id, task_id, alt_id).
		job_ends = []


		used = [[model.NewBoolVar(f'used {job_id} {task_id}') for task_id in range(len(self.jobs[job_id]))] for job_id in all_jobs]


		# Scan the jobs and create the relevant variables and intervals.
		for job_id in all_jobs:
			job = self.jobs[job_id]
			num_tasks = len(job)
			previous_end = None
			for task_id in range(num_tasks):

				task = job[task_id]

				min_duration = task[0][0]
				max_duration = task[0][0]

				num_alternatives = len(task)
				all_alternatives = range(num_alternatives)

				for alt_id in range(1, num_alternatives):
					alt_duration = task[alt_id][0]
					min_duration = min(min_duration, alt_duration)
					max_duration = max(max_duration, alt_duration)

				# Create main interval for the task.
				suffix_name = '_j%i_t%i' % (job_id, task_id)
				start = model.NewIntVar(0, horizon, 'start' + suffix_name)
				duration = model.NewIntVar(min_duration, max_duration,
										'duration' + suffix_name)
				end = model.NewIntVar(0, horizon, 'end' + suffix_name)
				interval = model.NewIntervalVar(start, duration, end,
												'interval' + suffix_name)


				if task[0][1] != -1:
					model.Add(end < 60).OnlyEnforceIf(used[job_id][task_id])
					model.Add(end >= 60).OnlyEnforceIf(used[job_id][task_id].Not())
				else:
					model.Add(used[job_id][task_id] == False)

				# Store the start for the solution.
				self.starts[(job_id, task_id)] = start

				# Add precedence with previous task in the same job.
				if previous_end is not None:
					model.Add(start >= previous_end)
				previous_end = end

				# Create alternative intervals.
				if num_alternatives > 1:
					l_presences = []
					for alt_id in all_alternatives:
						alt_suffix = '_j%i_t%i_a%i' % (job_id, task_id, alt_id)
						l_presence = model.NewBoolVar('presence' + alt_suffix)
						l_start = model.NewIntVar(0, horizon, 'start' + alt_suffix)
						l_duration = task[alt_id][0]
						l_end = model.NewIntVar(0, horizon, 'end' + alt_suffix)
						l_interval = model.NewOptionalIntervalVar(
							l_start, l_duration, l_end, l_presence,
							'interval' + alt_suffix)
						l_presences.append(l_presence)

						# Link the master variables with the local ones.
						model.Add(start == l_start).OnlyEnforceIf(l_presence)
						model.Add(duration == l_duration).OnlyEnforceIf(l_presence)
						model.Add(end == l_end).OnlyEnforceIf(l_presence)

						# Add the local interval to the right machine.
						if task[alt_id][1] not in intervals_per_resources.keys():
							intervals_per_resources[task[alt_id][1]] = []
						intervals_per_resources[task[alt_id][1]].append(l_interval)

						# Store the presences for the solution.
						self.presences[(job_id, task_id, alt_id)] = l_presence

					# Select exactly one presence variable.
					model.AddExactlyOne(l_presences)
				else:
					if task[0][1] not in intervals_per_resources.keys():
						intervals_per_resources[task[0][1]] = []
					intervals_per_resources[task[0][1]].append(interval)
					self.presences[(job_id, task_id, 0)] = model.NewConstant(1)

			job_ends.append(previous_end)
		# Create machines constraints.
		for machine_id in all_machines:
			intervals = intervals_per_resources[machine_id]
			if len(intervals) > 1:
				model.AddNoOverlap(intervals)


		model.Maximize(sum([sum(used[job_id]) for job_id in all_jobs]))

		# Solve model.
		self.solver = cp_model.CpSolver()

		self.solver.Solve(model)

	def print_sol(self):
		ans = ''
		K = 0
		# Print final solution.
		for job_id in range(len(self.jobs)):
			for task_id in range(len(self.jobs[job_id])):
				start_value = self.solver.Value(self.starts[(job_id, task_id)])
				machine = -1
				for alt_id in range(len(self.jobs[job_id][task_id])):
					if self.solver.Value(self.presences[(job_id, task_id, alt_id)]):
						machine = self.jobs[job_id][task_id][alt_id][1]
				if machine != -1:
					if start_value + self.subjects[self.classes[job_id].subjects[task_id]] <= 60:
						ans += f'{job_id+1} {self.classes[job_id].subjects[task_id]} {start_value+1} {machine+1}\n'
						K += 1
		print(K)
		print(ans)
	

# inp = file, if inp = False, => reading from input, out is output file, is_print: if print to console
def main():
	classes, teachers, subjects = import_data()
	
	sol = Solver(classes, teachers, subjects)

	sol.solve()

	sol.print_sol()

	

if __name__ == "__main__":

	main()
