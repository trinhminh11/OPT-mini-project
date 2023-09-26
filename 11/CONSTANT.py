random_seed = 11042004

#import data
def import_data(file):
    distance_matrix = []
    with open(file, 'r') as f:
        N, K = map(int, f.readline().split())

        for i in range(N+1):
            distance_matrix.append(list(map(float, f.readline().split())))
    
    return N, K, distance_matrix