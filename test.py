import numpy as np
from scipy.optimize import linear_sum_assignment

# Define your cost matrix with negated values
cost_matrix = np.array([
    [-1, -1],
    [-1, -1],
    [-1, -1]
])

print(cost_matrix.sum())