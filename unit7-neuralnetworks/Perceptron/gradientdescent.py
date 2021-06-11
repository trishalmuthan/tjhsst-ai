import sys
import math
import time
import numpy as np

def partial_deriv_Ax(x, y):
    return (8*x) - (3*y) + 24

def partial_deriv_Ay(x, y):
    return 4*(y-5) - (3*x)

def partial_deriv_Bx(x, y):
    return 2*(x-(y**2))

def partial_deriv_By(x, y):
    return 2*((-2*x*y) + (2*(y**3)) + y - 1)

def gradient_descent(input_vec, learning_rate, partial_deriv_x, partial_deriv_y):
    i = 0 
    while True:
        print(f'{i} - Current Location: {input_vec}')
        gradient = np.array([partial_deriv_x(input_vec[0], input_vec[1]), partial_deriv_y(input_vec[0], input_vec[1])])
        print(f'{i} - Current Gradient: {gradient}')
        if np.linalg.norm(gradient) < (1*(10**(-8))):
            break
        input_vec = input_vec-(learning_rate * gradient)
        i += 1
    print(f'Final Minimized Location: {input_vec}')

function = sys.argv[1]
if function == 'A':
    gradient_descent(np.array([0, 0]), 0.05, partial_deriv_Ax, partial_deriv_Ay)
else:
    gradient_descent(np.array([0, 0]), 0.05, partial_deriv_Bx, partial_deriv_By)
