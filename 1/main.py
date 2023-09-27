from CONSTANT import Staff, import_data

#class Solver, solve the problem
class Solver:
	def __init__(self, staff: list[Staff], D, A, B):
		self.N = len(staff)
		self.staff = staff
		self.D = D
		self.A = A 
		self.B = B

		#solution matrix
		self.X = [[-1 for _ in range(D)] for _ in range(self.N)]
	
	#calc minimum number of specific shift that all staff work on all Day
	def calc_min(self, shift):
		ans = float('inf')
		for ID in range(self.N):
			ans = min(ans, self.X[ID].count(shift))
		
		return ans
	

	#add at least A night shift to specific day
	def add_night_shift(self, day):
		num_Insert = 0
		#add all night shift to prev day of day off for each person
		for i in range(self.A):
			for person in self.staff:
				if self.X[person.ID-1][day-1] == -1:
					if day+1 in person.dayoff:
						self.X[person.ID-1][day-1] = 4
						num_Insert += 1
						break 
		
		min_shift = self.calc_min(4)

		# each slot in each day have at least A Staff
		while num_Insert < self.A:
			# loop through each person in staff
			for person in self.staff:
				if self.X[person.ID-1][day-1] == -1:

					# add min shift to this person in given day
					if self.X[person.ID-1].count(4) == min_shift:
						self.X[person.ID-1][day-1] = 4
						num_Insert += 1
						break
			
			min_shift = self.calc_min(4)
	
	# add day off to X
	def add_day_off(self, day):
		for ID, person in enumerate(self.staff):
			if day-2 < 0:
				if day in person.dayoff:
					self.X[ID][day-1] = 0
			else:
				if day in person.dayoff or self.X[ID][day-2] == 4:
					self.X[ID][day-1] = 0

	
	# fill every shift except night shift to specific day
	def first_fill(self, day):
		shift = 1
		count_shift = 0
		for person in self.staff:
			# if that shift reach minimum requirement, go to next shift
			if count_shift == self.A:
				shift += 1
				count_shift = 0
			
			# only add day shift, not night shift
			if shift < 4:
				if self.X[person.ID-1][day-1] == -1:
					self.X[person.ID-1][day-1] = shift
					count_shift += 1

	# for each day, after reaching minimum requirement, fill all the shift one by one
	def last_fill(self, day):
		shift = 1
		count_shift = self.A
		for person in self.staff:
			if shift < 4:
				if self.X[person.ID-1][day-1] == -1:
					self.X[person.ID-1][day-1] = shift
					shift += 1
			else:
				shift = 0
		


	#main solve function
	def solve(self):
		for day in range(1, self.D+1):
			#for each day, add night shift, and day off
			self.add_night_shift(day)
			self.add_day_off(day)
			#fill all day shift to the minimum requirement
			self.first_fill(day)
			#fill shift to all remain staff
			self.last_fill(day)
			
	
	def print_sol(self):
		for person in self.X:
			print(*person)
	
	def export(self, file):
		with open(file, 'w') as f:
			for row in self.X:
				for col in row:
					f.write(str(col))
					f.write(" ")
				f.write("\n")


def main():
	#staff, D: number of Day, each slot in each day have at least A Staff and at most B staff
	try:
		staff, D, A, B = import_data('1/test.txt')
	except:
		staff, D, A, B = import_data('test.txt')

	sol = Solver(staff, D, A, B)

	sol.solve()
	sol.print_sol()

	try:
		sol.export('1/output.txt')
	except:
		sol.export('output.txt')


if __name__ == "__main__":
	main()