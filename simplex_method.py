import numpy as np
import time

def convert(A, b, c, Q0):
    A = np.array(A)
    m, n = A.shape

    # Add slack variables
    slack_variables = np.eye(m)
    A_extended = np.hstack((A, slack_variables))
    c_extended = np.concatenate((c, np.zeros(m)))

    # Add surplus variables
    surplus_variables = np.eye(m)
    A_surplus = np.hstack((A, surplus_variables))
    XB = []
    for i in range (m):
        XB.append(len(c_extended)-m+i)
    tableau = np.vstack((np.hstack((np.zeros(1), -c_extended, 0)), np.column_stack((b, A_surplus, Q0*np.ones(m)))))
    return tableau

def update_tableau(tableau, basis):
    new_tableau = []
    
    for row_idx in range(len(basis) + 1):
        local_tableau = tableau[:]
        local_basis = basis[:]
        m = local_tableau[row_idx]
        rows = np.delete(local_tableau, row_idx, 0)
        
        if row_idx > 0:
            cur_intersection_value = m[local_basis[row_idx - 1]]
            del local_basis[row_idx - 1]
        
        if all(m[local_basis] == 0) and row_idx > 0:
            new_row = m / cur_intersection_value
        else:
            for row in rows:
                e = [e for e, i in enumerate(m[local_basis]) if i != 0]
                c = - m[local_basis][e] / row[local_basis][e]
                new_row = m + c * row
                
                if all(new_row[local_basis] == 0):
                    break
        
        new_tableau.append(new_row)
                
    return np.array(new_tableau)

def simplex_method(A, b, c, Q0):
        
    tableau = convert(A, b, c, Q0)

    while np.any(tableau[0, 1:] < 0):
        pivot_col = np.argmin(tableau[0, 1:]) + 1

        ratios = np.where(tableau[1:, pivot_col] > 0, tableau[1:, 0] / tableau[1:, pivot_col], np.inf)

        if np.all(ratios == np.inf):
            return False, None, None

        pivot_row = np.argmin(ratios) + 1

        pivot = tableau[pivot_row, pivot_col]

        tableau[pivot_row, :] /= pivot

        tableau = update_tableau(tableau, pivot)
        
        for i in range(tableau.shape[0]):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]

    optimal_solution = tableau[1:, 0]
    optimal_value = tableau[0, 0]

    return True, optimal_solution, optimal_value

from scipy.optimize import linprog

def simplex_method1(a, Q, c):
    A = -1 * np.array(a) 

    b = -1 * np.array(Q) 
    Q0 = max(Q)
    # Bounds for variables
    x0_bounds = (0, Q0)
    bounds = [x0_bounds] * len(c)

    # Solve the linear programming problem
    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if result.success:
        optimal_solution = [round(x, 6) for x in result.x]
        optimal_value = round(result.fun, 6)
    else:
        optimal_solution = None
        optimal_value = None

    return result.success, optimal_solution, optimal_value

'''test = {'A': np.array([[ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,
         1.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  1.,  1.],
       [ 1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  1.,  1.,  1.,  1.,  1.,
         1.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,
         1.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  1.,  0.],
       [ 0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,
         0.,  1.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  1.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,
         0.,  1.,  0.,  0.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,
         0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,
         0.,  0.,  1.,  0.,  0.,  0.,  1.,  0.,  0.,  1.,  1.,  1.,  1.,
         0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  1.],
       [ 0.,  0.,  0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  1.,  1.,  1.,
         1.,  0.,  0.,  1.,  1.,  1.,  0.,  1.,  1.,  1.,  1.,  0.,  1.,
         1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.,  1.,  1.],
       [ 1.,  0.,  1.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  1.,  1.,
         0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,
         1.,  1.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.],
       [ 0.,  0.,  0.,  1.,  0.,  0.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,
         1.,  0.,  0.,  0.,  1.,  0.,  0.,  1.,  1.,  1.,  0.,  0.,  1.,
         0.,  0.,  1.,  1.,  0.,  0.,  1.,  1.,  1.,  1.,  1.],
       [ 0.,  1.,  0.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  1.,  1.,  0.,  1.,  1.,  0.,  0.,  0.,
         0.,  1.,  0.,  1.,  1.,  0.,  0.,  0.,  1.,  1.,  1.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,
         0.,  0.,  0.,  0.,  0.,  1.,  1.,  0.,  0.,  0.,  1.],
       [-0., 1., -0., -0., -0., -0., -0., -0., -0., -0., -0., -0., -0.,
        -0., -0., -0., -0., -0., -0., -0., -0., -0., -0., -0., -0., -0.,
        -0., -0., -0., -0., -0., -0., -0., -0., -0., -0., -0.]]), 
        'b': np.array([5, 1, 3, 5, 5, 3, 3, 2, 1, 4, 1]), 
        'c': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        'Q0': 5}
print(len(test['A'][0]))
flag, optimal_solution, optimal_value = simplex_method(test['A'], test['b'], test['c'], test['Q0'])
print(flag)
print(optimal_solution)
print(optimal_value)'''