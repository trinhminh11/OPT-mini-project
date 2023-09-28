random_seed = 11042004

#import data
def import_data(file):
    distance_matrix = []
    cost_matrix = []
    with open(file, 'r') as f:
        N, M = map(int, f.readline().split())

        for i in range(N):
            cost_matrix.append(list(map(int, f.readline().split())))


        for i in range(M+1):
            distance_matrix.append(list(map(float, f.readline().split())))
        
        q = list(map(int, f.readline().split()))
    
    
    return N, M, cost_matrix, distance_matrix, q