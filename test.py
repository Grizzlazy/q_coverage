from scipy.optimize import linprog
import numpy as np
import data
file_name_csv = "Data/N=10_W=10_H=8_normal_0.csv"
T, Q = data.read_data(file_name_csv)

P, a, I = data.find_positions(T)
# Objective function coefficients
m = len(P)
c = [1] * m
# Inequality constraints matrix
def simplex_method(a, Q, c):
    A = -1 * np.array(a)  # Assuming 'a' is a matrix of coefficients

    # Inequality constraints RHS
    b = -1 * np.array(Q)  # Assuming 'q' is a vector of constants
    Q0 = max(Q)
    # Bounds for variables
    x0_bounds = (0, Q0)
    bounds = [x0_bounds] * m

    # Solve the linear programming problem
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if result.success:
        print("Optimization successfully converged.")
        optimal_solution = result.x
        optimal_value = result.fun
    else:
        print("Optimization did not converge. No solution found.")
        optimal_solution = None
        optimal_value = None

    return result.success, optimal_solution, optimal_value
'''
# Optimal solution
flag, optimal_solution, optimal_value = simplex_method(a, Q, c) 
print(flag)
print("Optimal Solution:", optimal_solution)
print("Optimal Value:", optimal_value)'''
