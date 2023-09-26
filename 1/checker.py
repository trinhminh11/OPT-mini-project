from CONSTANT import import_data, Staff

def count_day(X, day, shift):
    ans = 0

    for ID in range(len(X)):
        if X[ID][day] == shift:
            ans += 1
    
    return ans

def Checker(staff: list[Staff], D, A, B, X):
    #check format:
    if len(X) != len(staff):
        print("wrong format N")
        exit()
    
    for row in X:
        if len(row) != D:
            print("wrong format D")
            exit()
    

    for day in range(D):
        print(f"Day {day+1}:")
        for shift in range(1, 5):
            a = count_day(X, day, shift)
            if A <= a <= B:
                print(f'shift {shift}: {a}')
            else:
                print("here")
                exit()

        for person in staff:
            for d in person.dayoff:
                if X[person.ID-1][d-1] != 0:
                    print(f'Staff {person.ID} should have a day off at day {day+1}')
                    exit()
            
            if day < D-1:
                if X[person.ID-1][day] == 4 and X[person.ID-1][day+1] != 0:
                    print(f'Staff {person.ID} should have a day off at day {day+1}')
                    exit()
    


def import_output(file):
    X = []
    with open(file, 'r') as f:
        while True:
            temp = list(map(int, f.readline().split()))
            if temp == []:
                break
            X.append(temp)
    
    return X

def main():
    staff, D, A, B = import_data("1/test.txt")
    X = import_output('1/output.txt')



    Checker(staff, D, A, B, X)

if __name__ == "__main__":
    main()