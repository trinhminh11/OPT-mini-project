class Field:
	def __init__(self, ID, d, s, e):
		self.ID = ID
		self.product = d
		self.s = s
		self.e = e

		self.used = -1

def import_data():
	fields = []
	periods = {}
	
	N, m, M = map(int, input().split())

	min_day = float('inf')
	max_day = float('-inf')
	for i in range(N):
		d, s, e = map(int, input().split())
		fields.append(Field(i+1, d, s, e))
		if s < min_day:
			min_day = s
		if e > max_day:
			max_day = e
	
	for i in range(min_day, max_day+1):
		periods[i] = {'Field': [], 'total': 0}
		


	return fields, periods, m, M


class Solver:
	def __init__(self, fields, periods, m, M):
		self.fields = fields
		self.periods = periods
		self.m = m
		self.M = M
	
	# simple heuristic
	def solve(self):
		self.fields.sort(key= lambda x: [x.e, x.product])

		for period, _ in self.periods.items():
			# print(self.periods[period])
			for field in self.fields:
				if field.used == -1 and self.periods[period]['total'] + field.product <= self.M and field.s <= period and period <= field.e:
					self.periods[period]['Field'].append(field)
					self.periods[period]['total'] += field.product
					field.used = period

			# print(self.periods[period])
			
			if self.periods[period]['total'] < self.m:
				for field in self.periods[period]['Field']:
					field.used = -1
				
				self.periods[period]['Field'].clear()
				self.periods[period]['total'] = 0
		
		self.fields.sort(key=lambda x: x.ID)

	def print_sol(self):
		print(len(self.fields))

		for field in self.fields:
			print(field.ID, field.used)


def main():
	fields, periods, m, M = import_data()

	sol = Solver(fields, periods, m, M)

	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()
