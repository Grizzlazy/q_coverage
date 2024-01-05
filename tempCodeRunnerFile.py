    subproblem_floor, subproblem_ceil = create_subproblem(current_problem['A'], current_problem['b'], current_problem['c'], current_problem['Q0'], np.floor(current_solution))
            subproblem_ceil['Q0'] = current_solution
            subproblem_floor['Q0'] = current_solution
            pq.put((current_value, subproblem_floor))
            pq.put((current_value, subproblem_ceil))