from ortools.sat.python import cp_model

# Teacher class represent a Teacher, contain ID and all subjects of that teacher
class Teacher:
	def __init__(self, ID, subjects: list[int]):
		self.ID = ID
		self.subjects = subjects

		# dictionary with key = slot, value = True if this teacher busy on that slot and False if this teacher free
		self.used = [False for i in range(60)]

	# used for BnB
	def feasible(self, r):
		temp = [False for _ in range(r)]
		for i in range(len(self.used)):
			if self.used[i] == False:
				if self.used[i:i+r] == temp:
					return True
		
		return False
	
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

		self.used = [False for i in range(60)]


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
		


# import data, if file == False, read input, read file otherwise
def import_data(file):
	classes: list[Class] = []
	teachers: list[Teacher] = []

	if file:
		f = open(file, 'r')
		read = f.readline
	else:
		read = input
	
	T, N, M = map(int, read().split())

	for i in range(N):
		temp = list(map(int, read().split()))
		temp.pop()


		classes.append(Class(i+1, temp))
	
	for i in range(T):
		temp = list(map(int, read().split()))
		temp.pop()

		teachers.append(Teacher(i+1, temp))
	
	temp = list(map(int, read().split()))
	#dictionary key = subject ID, value = preiods
	subjects = {i+1: temp[i] for i in range(M)}
	
	find_possible_teachers(classes, teachers)

	if file:
		f.close()

	return classes, teachers, subjects


class Solver:
	def __init__(self, classes, teachers, subjects):
		self.classes = classes
		self.teachers = teachers
		self.subjects = subjects
		self.jobs = self.encode_data()
	
	# encode data
	def encode_data(self):
		# jobs[i][j][k] = (d, t)
		# i: classes[i]
		# j: index of subject in classes[i]
		# k: index of teacher can teach classes[i]-subjects[j
		# d: duration to learn classes[i]-subjects[j]
		# t: ID of classes[i]-subjects[j]-teachers[k]
		# (d, t) = (-1, -1) imply that there are no teacher to teach classes[i]-subjects[j]
		jobs = [
			[
				[
					(self.subjects[subject], teacher.ID-1) for teacher in c.teachers[subject]
				] if c.teachers[subject] else [(-1, -1)] for subject in c.subjects
			] for c in self.classes
		]
		
		# job is class, task is subject
		return jobs
		

	def solve(self):
		num_jobs = len(self.jobs)
		all_jobs = range(num_jobs)

		num_teachers = len(self.teachers)
		all_teachers = range(num_teachers)

		# Model
		model = cp_model.CpModel()


		# Global storage of variables.
		intervals_per_teacher = {} #T_intervals
		intervals_per_classes = {} #C_intervals
		self.starts = {}  # indexed by (job_idx, task_idx).
		self.presences = {}  # indexed by (job_idx, task_idx, alt_idx). #presences = 1 when in jobs[job_idx][task_idx] choose alt_idx to use, 0 otherwise

		self.used = []


		# Scan the jobs and create the relevant variables and intervals.
		for job_idx in all_jobs:
			job = self.jobs[job_idx]
			num_tasks = len(job)
			for task_idx in range(num_tasks):

				task = job[task_idx]

				# if there are no teacher to teach this jobs[job_idx][task_idx]
				if task[0] == (-1,-1):
					continue

				num_alternatives = len(task)
				all_alternatives = range(num_alternatives)


				suffix_name = '_j%i_t%i' % (job_idx, task_idx)


				start = model.NewIntVar(0, 60-task[0][0], 'start' + suffix_name)
				# Store the start for the solution.
				self.starts[(job_idx, task_idx)] = start	

				# Create alternative intervals.
				l_presences = []
				
				for alt_idx in all_alternatives:
					alt_suffix = '_j%i_t%i_a%i' % (job_idx, task_idx, alt_idx)
					# l_presence = 1 if jobs[job_idx][task_idx] use this alt_idx, 0 otherwise
					l_presence = model.NewBoolVar('presence' + alt_suffix)
					l_start = model.NewIntVar(0, 60 - task[alt_idx][0], 'start' + alt_suffix)
					l_duration = task[alt_idx][0]
					l_end = model.NewIntVar(0, 60, 'end' + alt_suffix)
					# interval var of this alt_idx
					l_interval = model.NewOptionalIntervalVar(
						l_start, l_duration, l_end, l_presence,
						'interval' + alt_suffix)
					
					l_presences.append(l_presence)

					# start//6 == (end-1)//6
					temp_s = model.NewIntVar(0, 9, "")
					temp_e = model.NewIntVar(0, 9, "")
					model.AddDivisionEquality(temp_s, l_start, 6) # temp_s = l_start // 6
					model.AddDivisionEquality(temp_e, l_end-1, 6) # temp_e = (l_end-1) // 6
					model.Add(temp_s == temp_e)

					# Link the master variables with the local ones.
					model.Add(start == l_start).OnlyEnforceIf(l_presence)

					# Add the local interval to the right teacher.
					if task[alt_idx][1] not in intervals_per_teacher.keys():
						intervals_per_teacher[task[alt_idx][1]] = []
					intervals_per_teacher[task[alt_idx][1]].append(l_interval)

					# Add the local interval to the right class
					if job_idx not in intervals_per_classes.keys():
						intervals_per_classes[job_idx] = []
					intervals_per_classes[job_idx].append(l_interval)

					# Store the presences for the solution.
					self.presences[(job_idx, task_idx, alt_idx)] = l_presence

				# Select one or none alt_idx in all_alt 
				model.Add(sum(l_presences) <= 1)

				self.used.append(sum(l_presences))


		# Create teachers constraints.
		for teacher_id in all_teachers:
			if teacher_id not in intervals_per_teacher.keys():
				continue

			intervals = intervals_per_teacher[teacher_id]

			if len(intervals) > 1:
				model.AddNoOverlap(intervals)
		
		# Create classes constraints
		for job_idx in all_jobs:
			if job_idx not in intervals_per_classes.keys():
				continue
			intervals = intervals_per_classes[job_idx]
			if len(intervals) > 1:
				model.AddNoOverlap(intervals)

		model.Maximize(sum(self.used))


		# Solve model.
		self.solver = cp_model.CpSolver()

		self.solver.parameters.max_time_in_seconds = 298


		status = self.solver.Solve(model)

		print(status == cp_model.OPTIMAL)

	def print_sol(self):
		ans = ''
		K = 0
		# Print final solution.
		for job_idx in range(len(self.jobs)):
			for task_idx in range(len(self.jobs[job_idx])):
				if self.jobs[job_idx][task_idx][0] == (-1, -1):
					continue
				start_value = self.solver.Value(self.starts[(job_idx, task_idx)])
				for alt_idx in range(len(self.jobs[job_idx][task_idx])):
					if self.solver.Value(self.presences[(job_idx, task_idx, alt_idx)]):
						machine = self.jobs[job_idx][task_idx][alt_idx][1]
						ans += f'{job_idx+1} {self.classes[job_idx].subjects[task_idx]} {start_value+1} {machine+1}\n'
						K += 1
						break 
						
		print(K)
		print(ans)
	
	def export_sol(self, file):
		ans = ''
		K = 0
		# Print final solution.
		for job_idx in range(len(self.jobs)):
			for task_idx in range(len(self.jobs[job_idx])):
				if self.jobs[job_idx][task_idx][0] == (-1, -1):
					continue
				start_value = self.solver.Value(self.starts[(job_idx, task_idx)])
				for alt_idx in range(len(self.jobs[job_idx][task_idx])):
					if self.solver.Value(self.presences[(job_idx, task_idx, alt_idx)]):
						machine = self.jobs[job_idx][task_idx][alt_idx][1]
						ans += f'{job_idx+1} {self.classes[job_idx].subjects[task_idx]} {start_value+1} {machine+1}\n'
						K += 1
						break

					
		
		with open(file, 'w') as f:
			f.write(str(K) + "\n")
			f.write(ans)
	

# inp = file, if inp = False, => reading from input, out is output file, is_print: if print to console
def main(inp, out, is_print):
	classes, teachers, subjects = import_data(inp)
	
	sol = Solver(classes, teachers, subjects)

	sol.solve()

	if is_print:
		sol.print_sol()

	if out:
		sol.export_sol(out)
	

if __name__ == "__main__":
	main(False, False, True)

