
# class Reviewer represent a reviewer have an ID and list of paper that this reviewer can review
class Reviewer:
	def __init__(self, ID):
		self.ID = ID
		self.papers = []

	#print for debug
	def __str__(self):
		ans = f"Reviewer {self.ID}\n"
		for paper in self.papers:
			ans += f'\tPaper {paper.ID}\n'
		return ans 

# class Paper represent a paper, have an ID and list of reviewers that willing to review this paper
class Paper:
	def __init__(self, ID):
		self.ID = ID
		self.reviewers = []

		# Solution contain reviewer that actually review this paper
		self.sol = []
	

	#print for debug
	def __str__(self):
		ans = f"Paper {self.ID}\n"
		for reviewer in self.reviewers:
			ans += f'\tReviewer {reviewer.ID}\n'
		return ans 

def import_data():
	papers = []
	reviewers = []
	N, M, b = map(int, input().split())

	for i in range(M):
		reviewers.append(Reviewer(i+1))

	for i in range(N):
		papers.append(Paper(i+1))
		IDs = list(map(int, input().split()))[1:]

		for ID in IDs:
			papers[i].reviewers.append(reviewers[ID-1])

			reviewers[ID-1].papers.append(papers[i])
	
	return papers, reviewers, b


# class Solver, solve the problem
class Solver:
	def __init__(self, papers, reviewers, b: int):
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
		count = {}
		print(len(self.papers))
		for paper in self.papers:
			print(self.b, end = " ")
			for reviewer in paper.sol:
				if reviewer.ID in count.keys():
					count[reviewer.ID] += 1
				else:
					count[reviewer.ID] = 1
				
				print(reviewer.ID, end = " ")
			print()

def main():
	papers, reviewers, b = import_data()

	sol = Solver(papers, reviewers, b)
	sol.solve()

	sol.print_sol()


if __name__ == "__main__":
	main()
