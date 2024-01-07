import data
import simplex_method
import queue
import math
import numpy as np
import copy

import matplotlib.pyplot as plt
file_name_csv = "Data/N=20_W=30_H=40_normal_0.csv"

T = [] #Target
Q = [] #Demand
I = [] #Target isolated
P = [] #Good position for placing sensors
x = [] #Number of sensors in P
a = [] #Sensor j cover by position P_i
T, Q = data.read_data(file_name_csv)

P, a = data.find_positions(T)
c = [1]*len(P)
epsilon = (-1)*0.000001

def isInteger(x):
    for i in range (len(P)):
        if not float(x[i]).is_integer():
            index = i
            return False, index
    return True, None

def create_subproblem(A, b, c, solution):
    index = isInteger(solution)[1]
    floor_constraint = np.zeros(len(P))
    floor_constraint[index] = 1

    subproblem_floor = {
        'A': np.vstack([A, floor_constraint]),
        'b': np.concatenate([b, [int(solution[index]) + 1]]),
        'c': c
    }

    ceil_constraint = -floor_constraint
    subproblem_ceil = {
        'A': np.vstack([A, ceil_constraint]),
        'b': np.concatenate([b, [-int(solution[index])]]),
        'c': c
    }

    return subproblem_floor, subproblem_ceil

def branch_and_bound(A, b, c):
    q = queue.Queue()
    iteration = 1e6
    best_value = 1e6
    best_solution = []
    initial_problem = {'A': A, 'b': b, 'c': c}
    q.put(initial_problem)
    while not q.empty():
        current_problem = q.get()
        flag, current_solution, current_value = simplex_method.simplex_method1(current_problem['A'], current_problem['b'], current_problem['c'])
        # print(flag, current_solution)
        if not flag: continue
        if isInteger(current_solution)[0]:
            if current_value - best_value < epsilon:
                best_solution = copy.deepcopy(current_solution)
                best_value = current_value
        else:
            if current_value - best_value < epsilon:
                subproblem_floor, subproblem_ceil = create_subproblem(current_problem['A'], current_problem['b'], current_problem['c'], current_solution)
                q.put(subproblem_floor)
                q.put(subproblem_ceil)
        #print('---------',iteration, '-----------')
        # print(current_value)
        # print(current_solution)
        #iteration -=1
    
    if best_solution == []:
        return False, None, None
    return True, best_solution, best_value

flag, x,  optimal_solution = branch_and_bound(a, Q, c)

def convert_output(x):
    output = []
    for i in range(len(P)):
        if x[i] != 0:
            output.append((P[i], x[i]))
    
    return output

output = convert_output(x)
if flag:
    for i in range(len(output)):
        print("Number of sensors in P",output[i][0]," is ", int(output[i][1]))
    
    print("Total sensors: ", int(optimal_solution))
# Create a new figure with specified size
plt.figure(figsize=(data.W, data.H))

# Set x-axis and y-axis limits based on W and H


for i in range(len(output)):
    center = np.array(output[i][0])
    theta = np.linspace(0, 2*np.pi, 100)
    x = (data.R+data.deltaR) * np.cos(theta) + center[0]
    y = (data.R+data.deltaR) * np.sin(theta) + center[1]   
    plt.plot(x, y, color = 'blue')
    if i == 0:
        plt.scatter(center[0], center[1], color='red', label = 'Sensors')
    else:
        plt.scatter(center[0], center[1], color='red')

for i in range(len(T)):
    if i == 0:
        plt.scatter(T[i][0], T[i][1], color='green', marker='*', label = 'Targets')
    else:
        plt.scatter(T[i][0], T[i][1], color='green', marker='*')

plt.axis([0, data.W, 0, data.H])
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.show()