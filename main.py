import data
import simplex_method
import queue
import math
import numpy as np

file_name_csv = "Data/N=10_W=10_H=8_normal_0.csv"

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


def isInteger(x):
    """
    As for a vector x,check if it contains only integer values:
    return the boolean value True and the None, i.e., [True,None] when the values are all integer
    return False and the index of the noninteger value in x, i.e., [False,index]

    """
    xx = np.array(x)
    dist = np.array(abs(np.rint(xx)-xx))
    for xx in dist:
        if float(xx).is_integer() == False:
            dist[dist == 0] = np.nan
            return (False, np.nanargmin(dist))
    return (True, None)

def create_subproblem(A, b, c, Q0, solution):
    # Create subproblem with rounded down constraints
    subproblem_floor = {
        'A': np.vstack([A, np.eye(len(c))]),
        'b': np.concatenate([b, np.floor(solution)]),
        'c': c,
        'Q0': Q0
    }

    # Create subproblem with rounded up constraints
    subproblem_ceil = {
        'A': np.vstack([A, -np.eye(len(c))]),
        'b': np.concatenate([b, -np.ceil(solution)]),
        'c': c,
        'Q0': Q0
    }

    return subproblem_floor, subproblem_ceil

def branch_and_bound(A, b, c, Q0):
    # Initialize priority queue
    pq = queue.PriorityQueue()
    tolerance=1e-6
    max_iterations=1000
    initial_problem = {'A': A, 'b': b, 'c': c, 'Q0': Q0}
    pq.put((0, initial_problem))

    best_solution = None
    best_value = float('inf')

    iterations = 0
    while not pq.empty() and iterations < max_iterations:
        # Pop problem with the best lower bound
        _, current_problem = pq.get()

        # Solve the current problem
        current_solution, current_value = simplex_method.simplex_method(current_problem['A'], current_problem['b'], current_problem['c'], current_problem['Q0'])

        # Update the best solution
        if np.all(current_value < best_value):
            best_solution = current_solution
            best_value = current_value

        # Check if the current solution is integer
        if all(np.abs(np.round(current_solution) - current_solution) < tolerance):
            continue  # Skip if the solution is integer

        # Branching - Create two subproblems
        subproblem_floor, subproblem_ceil = create_subproblem(current_problem['A'], current_problem['b'], current_problem['c'], current_problem['Q0'], np.floor(current_solution))
        subproblem_ceil['Q0'] = current_solution
        subproblem_floor['Q0'] = current_solution
        pq.put((current_value, subproblem_floor))
        pq.put((current_value, subproblem_ceil))

        iterations += 1

    return best_solution, best_value

x,  optimal_solution = branch_and_bound(a, Q, c, Q_0)

print(x)
print(optimal_solution)






    





