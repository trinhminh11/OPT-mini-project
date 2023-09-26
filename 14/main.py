from CONSTANT import import_data, Paper, Reviewer


class Solver:
    def __init__(self, papers: list[Paper], reviewers: list[Reviewer], b: int):
        self.papers = papers
        self.reviewers = reviewers
        self.b = b



    
    def solve(self):
        self.papers.sort(key=lambda x: len(x.reviewers))
        count_reviewers = {i+1: 0 for i in range(len(self.reviewers))}
        for _ in range(self.b):
            for paper in self.papers:
                paper.reviewers.sort(key=lambda x: [count_reviewers[x.ID], len(x.papers)])
                paper.sol.append(paper.reviewers[0])
                count_reviewers[paper.reviewers[0].ID] += 1
                paper.reviewers.pop(0)
            


        self.papers.sort(key=lambda x: x.ID)

    def print_sol(self):
        print(len(self.papers))

        for paper in self.papers:
            print(self.b, end = " ")
            for reviewer in paper.sol:
                print(reviewer.ID, end = " ")
            print()

    def export_sol(self, file):
        with open(file, 'w') as f:
            f.write(str(len(self.papers)) + "\n")

            for paper in self.papers:
                f.write(str(self.b) + " ")
                for reviewer in paper.sol:
                    f.write(str(reviewer.ID) + " ")

                f.write("\n")

def main():
    papers, reviewers, b = import_data("14/test.txt")

    sol = Solver(papers, reviewers, b)
    sol.solve()

    sol.print_sol()
    sol.export_sol('14/output.txt')

if __name__ == "__main__":
    main()