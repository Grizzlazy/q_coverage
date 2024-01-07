import numpy as np
from scipy.optimize import linprog
test = {'A': np.array([[ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  0.,  0.,  0.,  0.,  0.,
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
bounds = [(0, test['Q0']) for _ in range(len(test['c']))]
# Hàm chuyển bài toán về dạng chuẩn
def convert_to_standard_form(c, A, b, Q0):
    m, n = A.shape

    # Thêm biến giả và biến dư
    A_standard = np.hstack((A, np.eye(m)))
    c_standard = np.concatenate((c, np.zeros(m)))

    # Chuyển ràng buộc bất phương trình thành phương trình
    A_eq = np.hstack((A_standard, np.zeros((m, m))))
    b_eq = b

    # Chuyển ràng buộc x_i <= Q0 thành biểu diễn tách biến
    A_ineq = np.hstack((np.eye(m), np.zeros((m, m))))
    b_ineq = Q0 * np.ones(m)

    # Biến dư và biến giả đều phải là không âm
    bounds = [(0, None) for _ in range(n)] + [(None, None) for _ in range(m)] + [(0, None) for _ in range(m)]

    return c_standard, A_eq, b_eq, A_ineq, b_ineq, bounds

# Chuyển bài toán về dạng chuẩn
c_standard, A_eq, b_eq, A_ineq, b_ineq, bounds = convert_to_standard_form(test['c'], test['A'], test['b'], test['Q0'])

# Giải bài toán tối ưu hóa tuyến tính bằng linprog
result = linprog(c_standard, A_eq=A_eq, b_eq=b_eq, A_ub=A_ineq, b_ub=b_ineq, bounds=bounds, method='highs')

# Hiển thị kết quả
print("Optimal values of x:", result.x[:len(c)])
print("Optimal objective value:", result.fun)






