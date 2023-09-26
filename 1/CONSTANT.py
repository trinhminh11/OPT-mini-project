class Staff:
    def __init__(self, ID, dayoff):
        self.ID = ID
        self.dayoff = dayoff
    
    def __str__(self):
        ans = f"Staff {self.ID}: "
        for day in self.dayoff:
            ans += f'{day} '
        
        return ans 


def import_data(file):
    staff = []
    with open(file, 'r') as f:
        N, D, A, B = map(int, f.readline().split())
        for i in range(N):
            F = list(map(int, f.readline().split()))
            F.pop()
            staff.append(Staff(i+1, F))
    
    return staff, D, A, B
