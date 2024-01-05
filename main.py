import data
import simplex_method
import queue
import math
import numpy as np
import copy

file_name_csv = "Data/N=10_W=10_H=8_uniform_0.csv"

T = [] #Target
Q = [] #Demand
I = [] #Target isolated
P = [] #Good position for placing sensors
x = [] #Number of sensors in P
a = [] #Sensor j cover by position P_i
T, Q = data.read_data(file_name_csv)

P, a, I = data.find_positions(T)

c = [1]*len(P)
Q_0 = max(Q) #Highest demand
epsilon = (-1)*0.000001

def isInteger(x):
    xx = np.array(x)
    dist = np.array(abs(np.rint(xx) - xx))
    for i, val in enumerate(dist):
        if not float(val).is_integer():
            dist[dist == 0] = np.nan
            return False, np.nanargmin(dist)
    return True, None

def create_subproblem(A, b, c, Q0, solution):
    # Create subproblem with rounded down constraints
    index = isInteger(solution)[1]
    
    subproblem_floor = {
        'A': np.vstack([A, [0]*(index)+[1]+[0]*(len(P)-index-1)]),
        'b': np.concatenate([b, [int(solution[index])]]),
        'c': c,
        'Q0': Q0
    }
    # Create subproblem with rounded up constraints
    subproblem_ceil = {
        'A': np.vstack([A, [0]*(index)+[-1]+[0]*(len(P)-index-1)]),
        'b': np.concatenate([b, [-(int(solution[index])+1)]]),
        'c': c,
        'Q0': Q0
    }

    return subproblem_floor, subproblem_ceil


def branch_and_bound(A, b, c, Q0):
    q = queue.Queue()
    iteration = 1e6
    best_value = 1e6
    best_solution = []
    initial_problem = {'A': A, 'b': b, 'c': c, 'Q0': Q0}
    q.put(initial_problem)
    while not q.empty() and iteration > 0:
        current_problem = q.get()
        flag, current_solution, current_value = simplex_method.simplex_method(current_problem['A'], current_problem['b'], current_problem['c'], current_problem['Q0'])
        if not flag: continue
        if isInteger(current_solution)[0]:
            if current_value - best_value < epsilon:
                best_solution = copy.deepcopy(current_solution)
                best_value = current_value
            else: 
                continue
        else:
            if current_value - best_value > 0.01:
                continue
            subproblem_floor, subproblem_ceil = create_subproblem(current_problem['A'], current_problem['b'], current_problem['c'], current_problem['Q0'], current_solution)
            q.put(subproblem_floor)
            q.put(subproblem_ceil)
        print('---------',iteration, '-----------')
        print(current_value)
        print(current_solution)
        iteration -=1

    return best_solution, best_value

x,  optimal_solution = branch_and_bound(a, Q, c, Q_0)

print(x)
print(optimal_solution)