# -*- coding: utf-8 -*-
"""

Embry-Riddle Aeronautical University
@author: Nicolas Gachancipa

Dual Simplex Optimization Method
"""
# Imports
import numpy as np
from numpy import concatenate as ct

'''# Inputs
z = np.array([[2, 7, 6, 5, 0, 0, 0]])
A = np.array([[-2, 3, 5, 4, 1, 0, 0], 
              [7, 2, 6, -2, 0, 1, 0], 
              [-4, -5, 3, 2, 0, 0, 1]])
b = np.array([[-20, 35, -15]])
XB = [4, 5, 6]'''

a = [
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1]
]

# Bài toán tối ưu
b = [5, 1, 3, 5, 5, 3, 3, 2, 1, 4]
c = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

Q0 = 5

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
# Function to update tableau using matrix operations.
print(convert(a, b,c, Q0))
A, z, XB = convert(a, c)

def update_tableau(tableau, basis):
    
    # Create new tableau.
    new_tableau = []
    
    # Update each row (including z)
    for row_idx in range(len(basis) + 1):
        
        # Make a copy of the arrays.
        local_tableau = tableau[:]
        local_basis = basis[:]
        
        # Extract the row to edit (call it m).
        m = local_tableau[row_idx]
        
        # Remove that row form the tableau, and create a new array with 
        # the rest of the rows.
        rows = np.delete(local_tableau, row_idx, 0)
        
        # Obtain the intersection value for each basis element.
        # Only for the basis rows (i.e. row_idx > 0). Row index of z is 0.
        if row_idx > 0:
            
            # Obtain the value of the current row that must become one.
            # This is the value at the intersection of the basis element
            # rows and columns.
            cur_intersection_value = m[local_basis[row_idx - 1]]
        
            # Delete the intersection value.
            del local_basis[row_idx - 1]
            
        # If all basis column values in the current row are zero, and the 
        # column is not the objective function column (z)
        if all(m[local_basis] == 0) and row_idx > 0:
            
            # Divide the row by the intersection value.
            new_row = m/cur_intersection_value
        else:
            # Perform row operations to update the current row.
            for row in rows:
                e = [e for e, i in enumerate(m[local_basis]) if i != 0]
                c = - m[local_basis][e]/row[local_basis][e]
                new_row = m + c*row
                
                # Update until all basis column values are 0.
                if all(new_row[local_basis] == 0):
                    break
        
        # Append new row.
        new_tableau.append(new_row)
                
    # Return the new matrix.
    return np.array(new_tableau)
        
# Solve for the basis elements and update the A and b arrays.
for i, xb in enumerate(XB):
    basis_element = A[i][xb]
    if basis_element != 1:
        A[i] = A[i]/basis_element  
        b[0][i] /= basis_element

# Dual simplex method to find an optimal solution.
count = 2
z = np.array([list(z[0]) + [0]]) # Initialize solution to 0.

# Print initial tableau.
print('\n Tableau #1')
full_tableau = ct((z, ct((A, np.transpose(b)), axis = 1)))
print('Basis: ', XB)
print(full_tableau)

# Solve.
infeasible = False
while not all(b[0] > 0): 
    
    # Identify the element that leaves the basis.
    leaving = [i for i, y in enumerate(b[0] < 0) if y][0]
    
    # For the row that corresponds to the element that is leaving the 
    # basis, identify the elements that are negative.
    col_idxs = [i for i, y in enumerate(A[leaving] < 0) if y]
    negatives = A[leaving][col_idxs]
    
    # If there are no negatives in the row, the problem is infeasible.
    # Break.
    if len(negatives) == 0:
        infeasible = True
        print('Infeasible solution.')
        break 
    
    # Use the minimum ratio test to determine the element entering the basis.
    d = abs(np.divide(z[0][col_idxs], negatives))   
    entering = col_idxs[np.argmin(d)]
    
    # Update the basis.
    XB[leaving] = entering 
    
    # Update the tableau.
    full_tableau = ct((z, ct((A, np.transpose(b)), axis = 1)))
    full_tableau = update_tableau(full_tableau, XB)
    
    # Extract the new vectors and matrices from the tableau.
    z = np.expand_dims(full_tableau[0], 0)
    A = full_tableau[1:, :-1]
    b = np.transpose(full_tableau[1:, -1:])
    
    # Print the new tableau.
    print('\n Tableau #', count)
    print('Basis: ', XB)
    print(full_tableau)
    count += 1
    
# Print solutions.
if not infeasible:
    print('\n Primal solution:')
    for e, i in enumerate(b[0], 1):
        print('X%d = %f' % (e, i))
    print('z = ', -1*z[0][-1])
        
    print('\n Dual solution:')
    ct = 1
    for e, i in enumerate(z[0][:-1], 0):
        if e not in XB: 
            print('Y%d = %f' % (ct, z[0][e]*-1))
            ct += 1
    print('w = ', -1*z[0][-1])
