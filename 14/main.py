from CONSTANT import import_data, Paper, Reviewer

# class Solver, solve the problem
class Solver:
	def __init__(self, papers: list[Paper], reviewers: list[Reviewer], b: int):
		self.papers = papers
		self.reviewers = reviewers
		self.b = b

	# main solve function
	def solve(self):
		# sort paper bases on number of reviewers willing to review
		self.papers.sort(key=lambda x: len(x.reviewers))

		# count_papers dictionary with key = reviewer, value = number of paper that this reviewer review
		count_papers = {i+1: 0 for i in range(len(self.reviewers))}

		# run b times
		for _ in range(self.b):
			# loop through each paper
			for paper in self.papers:
				# get the minimum of paper.reviewers base on number of paper that reviewer review, and length of all paper that reviewer can review -> minimize 1 papers that 1 reviewer have to review
				reviewer = min(paper.reviewers, key=lambda x:[count_papers[x.ID], len(x.papers)] )
				# add that reviewer to solution reviewer of that paper
				paper.sol.append(reviewer)
				# add 1 to that count_papers's reviewer
				count_papers[reviewer.ID] += 1
				# remove reviewer from list reviewer willing to review the paper
				paper.reviewers.remove(reviewer)
			
		self.papers.sort(key=lambda x: x.ID)

	# printing solution
	def print_sol(self):
		print(len(self.papers))

		for paper in self.papers:
			print(self.b, end = " ")
			for reviewer in paper.sol:
				print(reviewer.ID, end = " ")
			print()

	# exporting solution
	def export_sol(self, file):
		with open(file, 'w') as f:
			f.write(str(len(self.papers)) + "\n")

			for paper in self.papers:
				f.write(str(self.b) + " ")
				for reviewer in paper.sol:
					f.write(str(reviewer.ID) + " ")

				f.write("\n")

def main():
	try:
		papers, reviewers, b = import_data("14/test.txt")
	except:
		papers, reviewers, b = import_data("test.txt")

	sol = Solver(papers, reviewers, b)
	sol.solve()

	sol.print_sol()

	try:
		sol.export_sol('14/output.txt')
	except:
		sol.export_sol('output.txt')

if __name__ == "__main__":
	main()