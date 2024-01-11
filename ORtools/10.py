from ortools.sat.python import cp_model

# class Class represent a class, contain ID, t: number of preiods, g: teacher ID, s: number of student
class Class:
	def __init__(self, ID, t, g, s):
		self.ID = ID
		self.time = t
		self.teacher = g 
		self.num_students = s
		# list of possible room
		self.rooms = []

	# print for debug
	def __str__(self):
		return f'class {self.ID}, preiods: {self.t}, teach by {self.g}, number of student {self.s}'



# import data
def import_data():
	classes = []

	rooms_cap = []


	N, M = map(int, input().split())
	for i in range(N):
		t, g, s = map(int, input().split())

		classes.append(Class(i+1, t, g, s))


	rooms_cap = list(map(int, input().split()))

	
	for c in classes:
		for room_idx, room_cap in enumerate(rooms_cap):
			if c.num_students <= room_cap:
				c.rooms.append(room_idx+1)
	
	return classes


class Solver:
	def __init__(self, classes):
		self.classes = classes
		self.jobs = self.encode_data()
	
	# encode data
	def encode_data(self):
		jobs = [
				[
					(c.time, room, c.teacher) for room in c.rooms
				] if c.rooms else [(-1, -1, -1)] 
				for c in self.classes
			] 
		
		
		# for job in jobs:
		# 	print('job:')
		# 	print(job)
		
		# exit()
		
		return jobs
		

	def solve(self):
		

		# Model the flexible jobshop problem.
		model = cp_model.CpModel()


		# Global storage of variables.
		intervals_per_room = {}
		intervals_per_teacher = {}

		self.starts = {}  # indexed by (job_id).
		self.presences = {}  # indexed by (job_id, alt_id).

		num_jobs = len(self.jobs)
		all_jobs = range(num_jobs)

		for job_idx in all_jobs:
			job = self.jobs[job_idx]

			num_alt = len(job)
			all_alt = range(num_alt)

			duration = job[0][0]

			start = model.NewIntVar(0, 60-duration, 'start')
			# Store the start for the solution.
			self.starts[job_idx] = start	

			# Create alternative intervals.
			l_presences = []

			for alt_idx in all_alt:
				room_ID = job[alt_idx][1]
				teacher_ID = job[alt_idx][2]

				alt_suffix = '_j%i_a%i' % (job_idx, alt_idx)
				# l_presence = 1 if jobs[job_idx] use this alt_idx, 0 otherwise
				l_presence = model.NewBoolVar('presence' + alt_suffix)
				l_start = model.NewIntVar(0, 60 - duration, 'start' + alt_suffix)
				l_end = model.NewIntVar(0, 60, 'end' + alt_suffix)
				# interval var of this alt_idx
				l_interval = model.NewOptionalIntervalVar(
					l_start, duration, l_end, l_presence,
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
				if teacher_ID not in intervals_per_teacher.keys():
					intervals_per_teacher[teacher_ID] = []
				intervals_per_teacher[teacher_ID].append(l_interval)

				# Add the local interval to the right room
				if room_ID not in intervals_per_room.keys():
					intervals_per_room[room_ID] = []
				intervals_per_room[room_ID].append(l_interval)

				# Store the presences for the solution.
				self.presences[(job_idx, alt_idx)] = l_presence
			
			model.Add(sum(l_presences) <= 1)
		

		for intervals in intervals_per_teacher.values():
			if len(intervals) > 1:
				model.AddNoOverlap(intervals)
		
		for intervals in intervals_per_room.values():
			if len(intervals) > 1:
				model.AddNoOverlap(intervals)


			
		model.Maximize(sum(self.presences.values()))


		# Solve model.
		self.solver = cp_model.CpSolver()

		self.solver.parameters.max_time_in_seconds = 298

		self.solver.Solve(model)

	def print_sol(self):
		ans = ''
		K = 0

		for job_idx in range(len(self.jobs)):
			start_value = self.solver.Value(self.starts[job_idx])
			room = -1

			for alt_idx in range(len(self.jobs[job_idx])):
				if self.solver.Value(self.presences[(job_idx, alt_idx)]):
					room = self.jobs[job_idx][alt_idx][1]
			
			if room != -1:
				ans += f'{job_idx+1} {start_value+1} {room}\n'

				K += 1

		print(K)
		print(ans)
	

def main():
	classes = import_data()
	sol = Solver(classes)

	sol.solve()

	sol.print_sol()
	

if __name__ == "__main__":
	main()