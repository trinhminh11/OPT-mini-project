from CONSTANT import Staff, import_data

class Solver:
	def __init__(self, staff, D, A, B):
		self.N = len(staff)
		self.staff: list[Staff] = staff
		self.D = D
		self.A = A 
		self.B = B
		self.X = [[-1 for _ in range(D)] for _ in range(self.N)]
	
	def calc_min(self, shift):
		ans = float('inf')
		for ID in range(self.N):
			ans = min(ans, self.X[ID].count(shift))
		
		return ans

	
	def add_night_shift(self, day):
		num_Insert = 0
		for i in range(self.A):
			for person in self.staff:
				if self.X[person.ID-1][day-1] == -1:
					if day+1 in person.dayoff:
						self.X[person.ID-1][day-1] = 4
						num_Insert += 1
						break 
		
		self.auto_fill(day, 4, num_Insert)
	
	def add_day_off(self, day):
		for ID, person in enumerate(self.staff):
			if day-2 < 0:
				if day in person.dayoff:
					self.X[ID][day-1] = 0
			else:
				if day in person.dayoff or self.X[ID][day-2] == 4:
					self.X[ID][day-1] = 0
	
	def auto_fill(self, day, shift, num_Insert = 0):
		
		min_shift = self.calc_min(shift)

		while num_Insert < self.A:
			for _ in range(self.A-num_Insert):
				for person in self.staff:
					if self.X[person.ID-1][day-1] == -1:
						
						if self.X[person.ID-1].count(shift) == min_shift:
							self.X[person.ID-1][day-1] = shift
							num_Insert += 1
							break
			
			min_shift = self.calc_min(shift)
	
	def first_fill(self, day):
		shift = 1
		count_shift = 0
		for person in self.staff:
			if count_shift == self.A:
				shift += 1
				count_shift = 0
			
			if shift < 4:
				if self.X[person.ID-1][day-1] == -1:
					self.X[person.ID-1][day-1] = shift
					count_shift += 1

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
		


	def solve(self):
		for day in range(1, self.D+1):
			self.add_night_shift(day)
			self.add_day_off(day)
			self.first_fill(day)
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
	staff, D, A, B = import_data('1//test.txt')

	sol = Solver(staff, D, A, B)

	for person in staff:
		print(person)

	sol.solve()
	sol.print_sol()
	sol.export('1/output.txt')


if __name__ == "__main__":
	main()