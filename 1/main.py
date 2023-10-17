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

		self.remaining = len(self.staff) * self.D
	
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
				if self.X[person.ID-1][day-1] == -1 and day not in person.dayoff:
					if day + 1 in person.dayoff:
						self.X[person.ID-1][day-1] = 4
						num_Insert += 1
						self.remaining -= 1
						break
		
		min_shift = self.calc_min(4)

		if day < self.D:

			# each slot in each day have at least A Staff
			while num_Insert < self.A:
				check_add = False
				# loop through each person in staff
				for person in self.staff:
					if self.X[person.ID-1][day-1] == -1 and self.X[person.ID-1][day] == -1:
						# add min shift to this person in given day
						if self.X[person.ID-1].count(4) == min_shift:
							self.X[person.ID-1][day-1] = 4
							self.X[person.ID-1][day] = 0

							num_Insert += 1
							self.remaining -= 2
							check_add = True
							break
						
				if check_add:
					min_shift = self.calc_min(4)
				else:
					min_shift += 1
					
		else:
			while num_Insert < self.A:
				check_add = False
				# loop through each person in staff
				for person in self.staff:
					if self.X[person.ID-1][day-1] == -1:
						# add min shift to this person in given day
						if self.X[person.ID-1].count(4) == min_shift:
							self.X[person.ID-1][day-1] = 4

							num_Insert += 1
							self.remaining -= 1
							check_add = True
							break
				
				if check_add:
					min_shift = self.calc_min(4)
				else:
					min_shift += 1

				
	
	# add day off to X
	def add_day_off(self, day):
		for person in self.staff:
			if day in person.dayoff:

				if self.X[person.ID-1][day-1] != -1:
					print(self.X[person.ID-1][day-1])
					print(person.ID, day)
					print("WTF")
					exit()

				self.X[person.ID-1][day-1] = 0
				self.remaining -= 1

	def count_shiff(self, shiff):
		count = 0
		for person in self.staff:

			count += self.X[person.ID-1].count(shiff)
		
		return count

	def add_more_day_off(self, day):

		for person in self.staff:
			if self.X[person.ID-1][day-1] == -1:
				self.X[person.ID-1][day-1] = 0
				return
			
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

		for person in self.staff:
			if shift < 4:
				if self.X[person.ID-1][day-1] == -1:
					self.X[person.ID-1][day-1] = shift
					shift += 1

			else:
				shift = 1
				
				if self.X[person.ID-1][day-1] == -1:
					self.X[person.ID-1][day-1] = shift
					shift += 1
	
	#main solve function
	def solve(self):
		for day in range(1, self.D+1):
			#for each day, add night shift, and day off
			self.add_day_off(day)
			self.add_night_shift(day)
		
		

		add_more = self.remaining // (self.B*3)

		while add_more > 0:
			for day in range(1, self.D+1):
				self.add_more_day_off(day)
				add_more -= 1
		
		for day in range(1, self.D+1):
			#fill all day shift to the minimum requirement
			self.first_fill(day)
			# #fill shift to all remain staff
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


def main(inp, out):
	#staff, D: number of Day, each slot in each day have at least A Staff and at most B staff
	staff, D, A, B = import_data(inp)

	sol = Solver(staff, D, A, B)

	sol.solve()
	
	sol.print_sol()

	sol.export(out)


if __name__ == "__main__":
	inp = f'test.txt'
	out = f'output.txt'
	main(inp, out)