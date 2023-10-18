from CONSTANT import import_data, Council, Thesis


class Solver:
	def __init__(self, thesises: list[Thesis], t, councils: list[Council]):
		self.thesises = thesises
		self.councils = councils
		self.teachers = {i+1: 0 for i in range(len(councils[0].possible_tea))}
		self.t = t

	def teacher2council(self):
		for i in range(len(self.councils)):
			self.councils[i].sol_teachers.append(i+1)
			self.teachers[i+1] = self.councils[i].ID
			self.councils[i].possible_thes.remove(self.t[i])

		rs = [i+1 for i in range(len(self.councils))]		
		for council in self.councils:
			for r in rs:
				council.possible_tea.remove(r)

		
		for teacher in self.teachers.keys():
			if self.teachers[teacher] != 0:
				continue

			best_council = None
			best_loss = float('inf')
			for council in self.councils:
				if len(council.sol_teachers) >= council.tea_bound[1]:
					continue

				current_loss = 0
				for thesis_ID in council.possible_thes:
					if teacher not in self.thesises[thesis_ID-1].tea_similarity.keys():
						current_loss += 1
				
				if len(council.possible_thes) - current_loss >= council.thes_bound[0]:
					if current_loss < best_loss:
						best_loss = current_loss
						best_council = council
			
			best_council.sol_teachers.append(teacher)

			rthesis = []
			for thesis_ID in best_council.possible_thes:
				if teacher not in self.thesises[thesis_ID-1].tea_similarity.keys():
					rthesis.append(thesis_ID)
			
			for r in rthesis:
				best_council.possible_thes.remove(r)
			
			self.teachers[teacher] = best_council.ID

	
	def thesis2council(self):


		for thesis in self.thesises:
			for council in self.councils:
				if thesis.ID in council.possible_thes and len(council.sol_thesises) < council.thes_bound[0]:
					council.add_thesis(thesis)
					thesis.council = council.ID
					break
		
		council_index = 0
		for thesis in self.thesises:
			if thesis.council:
				continue

			thesis.council = self.councils[council_index % len(self.councils)].ID

			council_index += 1

	def solve(self):
		self.thesises.sort(reverse=True, key= lambda x: [sum(x.thes_similarity.values()), sum(x.tea_similarity.values())])

		self.teacher2council()

		self.thesis2council()


	def print_sol(self):
		print(len(self.thesises))

		for thesis in self.thesises:
			print(thesis.council, end = " ")

		print()
		print(len(self.teachers))
		ans_teacher = [*self.teachers.values()]
		print(*ans_teacher)

		# for i in range(1, 60):
		# 	print(i, ans_teacher.count(i))



	def export_sol(self, file):
		pass

def main(inp, out):
	thesises, t, councils = import_data(inp)

	sol = Solver(thesises, t, councils)

	sol.solve()

	sol.print_sol()

	sol.export_sol(out)

if __name__ == "__main__":

	inp = f'input.txt'
	out = f'output.txt'
	main(inp, out)