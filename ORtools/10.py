import collections
from ortools.sat.python import cp_model

# class Class represent a class, contain ID, t: number of preiods, g: teacher ID, s: number of student
class Class:
	def __init__(self, ID, t, g, s):
		self.ID = ID
		self.time = t
		self.teacher = g 
		self.num_students = s
		# list of possible room
		self.rooms: list[Room] = []

	# print for debug
	def __str__(self):
		return f'class {self.ID}, preiods: {self.t}, teach by {self.g}, number of student {self.s}'

# class Room represent a Room, contain ID and capacity
class Room:
	def __init__(self, ID, capacity):
		self.ID = ID
		self.capacity = capacity

class Teacher:
	def __init__(self, ID):
		self.ID = ID

	
	def __str__(self):
		return f'Teacher {self.ID}'


# import data
def import_data():
	classes: list[Class] = []
	teachers: dict[int, Teacher] = {}
	rooms: list[Room] = []


	N, M = map(int, input().split())
	for i in range(N):
		t, g, s = map(int, input().split())

		classes.append(Class(i+1, t, g, s))

		if g not in teachers.keys():
			teachers[g] = Teacher(g)


	temp = list(map(int, input().split()))

	for i, capacity in enumerate(temp):
		rooms.append(Room(i+1, capacity))
	
	for c in classes:
		for room in rooms:
			if c.num_students <= room.capacity:
				c.rooms.append(room)
	
	return classes, teachers, rooms


class Solver:
	def __init__(self, classes: list[Class], teachers: list[Teacher], rooms: list[int]):
		self.classes = classes
		self.teachers = teachers
		self.rooms = rooms
		self.jobs = self.encode_data()
	
	# encode data
	def encode_data(self):
		jobs = [
			[
				[
					(c.time, room.ID-1) for room in c.rooms
				] if c.rooms else [(0, -1)] 
			] for c in self.classes
		]
		
		# for job in jobs:
		# 	print('job:')
		# 	for task in job:
		# 		print(task)
		
		# exit()
		
		return jobs
		

	def solve(self):
		num_jobs = len(self.jobs)
		all_jobs = range(num_jobs)

		num_machines = len(self.rooms)
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
		intervals_per_room = collections.defaultdict(list)
		intervals_per_teacher = collections.defaultdict(list)
		self.starts = {}  # indexed by (job_id, task_id).
		self.presences = {}  # indexed by (job_id, task_id, alt_id).
		job_ends = []

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

				duration = self.classes[job_id].time

				end = model.NewIntVar(0, horizon, 'end' + suffix_name)
				interval = model.NewIntervalVar(start, duration, end,
												'interval' + suffix_name)

				intervals_per_teacher[self.classes[job_id].teacher].append(interval)

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
						l_end = model.NewIntVar(0, horizon, 'end' + alt_suffix)
						l_interval = model.NewOptionalIntervalVar(
							l_start, duration, l_end, l_presence,
							'interval' + alt_suffix)
						l_presences.append(l_presence)

						# Link the master variables with the local ones.
						model.Add(start == l_start).OnlyEnforceIf(l_presence)
						model.Add(end == l_end).OnlyEnforceIf(l_presence)

						# Add the local interval to the right machine.
						intervals_per_room[task[alt_id][1]].append(l_interval)

						# Store the presences for the solution.
						self.presences[(job_id, task_id, alt_id)] = l_presence

					# Select exactly one presence variable.
					model.AddExactlyOne(l_presences)

				else:
					intervals_per_room[task[0][1]].append(interval)
					self.presences[(job_id, task_id, 0)] = model.NewConstant(1)

			job_ends.append(previous_end)

		# Create machines constraints.
		for machine_id in all_machines:
			intervals = intervals_per_room[machine_id]
			if len(intervals) > 1:
				model.AddNoOverlap(intervals)
		# teacher constraints
		for teacher_id in intervals_per_teacher:
			intervals = intervals_per_teacher[teacher_id]
			if len(intervals) > 1:
				model.AddNoOverlap(intervals)

		# Makespan objective
		makespan = model.NewIntVar(0, horizon, 'makespan')
		model.AddMaxEquality(makespan, job_ends)
		model.Minimize(makespan)

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
				if machine != -1 and start_value + self.classes[job_id].time < 60:
					ans += f'{job_id+1} {start_value+1} {machine+1}\n'
					K += 1	
		print(K)
		print(ans)
	

def main():
	classes, teachers, rooms = import_data()
	sol = Solver(classes, teachers, rooms)

	sol.solve()

	sol.print_sol()
	

if __name__ == "__main__":
	main()