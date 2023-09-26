# class Staff represent ID of staff and list of days off of that staff
class Staff:
    def __init__(self, ID, dayoff):
        self.ID = ID
        self.dayoff = dayoff
    
    #printing for debug
    def __str__(self):
        ans = f"Staff {self.ID}: "
        for day in self.dayoff:
            ans += f'{day} '
        
        return ans 


#import data
def import_data(file):
    #list of staff
    staff: list[Staff] = []
    with open(file, 'r') as f:
        #N: number of Staff, D: number of Day, each slot in each day have at least A Staff and at most B staff
        N, D, A, B = map(int, f.readline().split())
        for i in range(N):
            F = list(map(int, f.readline().split()))
            F.pop()
            staff.append(Staff(i+1, F))
    
    return staff, D, A, B
