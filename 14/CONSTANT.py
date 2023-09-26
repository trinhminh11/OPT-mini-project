
# class Reviewer represent a reviewer have an ID and list of paper that this reviewer can review
class Reviewer:
	def __init__(self, ID):
		self.ID = ID
		self.papers: list[Paper] = []

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
		self.reviewers: list[Reviewer] = []

		# Solution contain reviewer that actually review this paper
		self.sol: list[Reviewer] = []
	

	#print for debug
	def __str__(self):
		ans = f"Paper {self.ID}\n"
		for reviewer in self.reviewers:
			ans += f'\tReviewer {reviewer.ID}\n'
		return ans 

def import_data(file):
	papers:list[Paper] = []
	reviewers: list[Reviewer] = []
	with open(file, 'r') as f:
		N, M, b = map(int, f.readline().split())

		for i in range(M):
			reviewers.append(Reviewer(i+1))

		for i in range(N):
			papers.append(Paper(i+1))
			IDs = list(map(int, f.readline().split()))[1:]

			for ID in IDs:
				papers[i].reviewers.append(reviewers[ID-1])

				reviewers[ID-1].papers.append(papers[i])
	
	return papers, reviewers, b

