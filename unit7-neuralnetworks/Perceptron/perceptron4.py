import sys
import math
import time
import random
import ast
import numpy as np

def step(num):
    if num > 0:
        return 1
    else:
        return 0

def sigmoid(num):
    return 1/(1+math.exp(-num))

def p_net(A, x, w_list, b_list):
    vectorized_A = np.vectorize(A)
    a = x
    for l in range(1, len(w_list)):
        a = vectorized_A((a@w_list[l]) + b_list[l])
        print(a)
    #print(a[0])
    return round(a[0])

def do_circle(array):
    if math.sqrt((array[0])**2 + (array[1])**2) < 1:
        return 1
    else:
        return 0

def check_circle(w_list, b_list):
    num_correct = 0
    for i in range(500):
        random_x = random.uniform(-1, 1)
        random_y = random.uniform(-1, 1)
        test = np.array([random_x, random_y])
        if do_circle(test) == p_net(sigmoid, test, w_list, b_list):
            num_correct += 1
        else:
            print(f'Coordinate {i}: {test}')
    print(f'Circle Accuracy: {num_correct / 500}')

#CIRCLE HAPPENS HERE
if len(sys.argv) == 1: #circle check (challenge 3)
    w_list = [None, np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]), np.array([[1], [1], [1], [1]])]
    b_list = [None, np.array([1.5, 1.5, 1.5, 1.5]), np.array([-3.1])]
    check_circle(w_list, b_list)

#XOR HAPPENS HERE
elif len(sys.argv) == 2: #xor check (challenge 1)
    x = np.array(list(ast.literal_eval(sys.argv[1])))
    w_list = [None, np.array([[2, -1], [2, -1]]), np.array([[1], [1]])]
    b_list = [None, np.array([-1, 2]), np.array([-1])]
    xor_output = p_net(step, x, w_list, b_list)
    print(xor_output)

#DIAMOND HAPPENS HERE
else: #diamond check (challenge 2)
    x = np.array([float(sys.argv[1]), float(sys.argv[2])])
    w_list = [None, np.array([[-1, 1, 1, -1], [-1, -1, 1, 1]]), np.array([[1], [1], [1], [1]])]
    b_list = [None, np.array([1, 1, 1, 1]), np.array([-3])]
    output = p_net(step, x, w_list, b_list)
    if output == 1:
        print('Inside')
    else:
        print('Outside')

