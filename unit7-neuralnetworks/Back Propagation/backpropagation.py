import sys
import math
import time
import random
import numpy as np

def sigmoid_deriv(num):
    return sigmoid(num) * (1 - sigmoid(num))

def sigmoid(num):
    return 1/(1+math.exp(-num))

def sum_train(w_list, b_list, training_set, epochs, learning_rate, A, A_deriv):
    vectorized_A = np.vectorize(A)
    vectorized_A_deriv = np.vectorize(A_deriv)
    for epoch in range(epochs):
        print(f'Epoch {epoch}:')
        for x, y in training_set:
            a = x
            dots = [None]
            a_list = [a]
            for l in range(1, len(w_list)):
                dot_l = (a@w_list[l]) + b_list[l]
                dots.append(dot_l)
                a = vectorized_A(dot_l)
                a_list.append(a)
            print(a)
            error = 0.5*(np.linalg.norm(y-a) ** 2)
            delta_n = vectorized_A_deriv(dots[-1]) * (y - a)
            delta_l_list = [delta_n]
            for l in range(len(w_list)-2, 0, -1):
                delta_l = vectorized_A_deriv(dots[l])*(delta_l_list[-1]@(w_list[l+1].transpose()))
                delta_l_list.append(delta_l)
            delta_l_list.append(None)
            delta_l_list = delta_l_list[::-1]
            for l in range(1, len(w_list)):
                b_list[l] = b_list[l] + (learning_rate * delta_l_list[l])
                w_list[l] = w_list[l] + (learning_rate * (a_list[l-1].transpose() @ delta_l_list[l]))
    return w_list, b_list

def circle_train(w_list, b_list, training_set, epochs, learning_rate, A, A_deriv):
    vectorized_A = np.vectorize(A)
    vectorized_A_deriv = np.vectorize(A_deriv)
    for epoch in range(epochs):
        print(f'Epoch {epoch}:')
        for x, y in training_set:
            a = x
            dots = [None]
            a_list = [a]
            for l in range(1, len(w_list)):
                dot_l = (a@w_list[l]) + b_list[l]
                dots.append(dot_l)
                a = vectorized_A(dot_l)
                a_list.append(a)
            error = 0.5*(np.linalg.norm(y-a) ** 2)
            delta_n = vectorized_A_deriv(dots[-1]) * (y - a)
            delta_l_list = [delta_n]
            for l in range(len(w_list)-2, 0, -1):
                delta_l = vectorized_A_deriv(dots[l])*(delta_l_list[-1]@(w_list[l+1].transpose()))
                delta_l_list.append(delta_l)
            delta_l_list.append(None)
            delta_l_list = delta_l_list[::-1]
            for l in range(1, len(w_list)):
                b_list[l] = b_list[l] + (learning_rate * delta_l_list[l])
                w_list[l] = w_list[l] + (learning_rate * (a_list[l-1].transpose() @ delta_l_list[l]))
        classify_circle(w_list, b_list, training_set, A)

def classify_circle(w_list, b_list, dataset, A):
    vectorized_A = np.vectorize(A)
    correct = 0
    for x, y in dataset:
        a = x
        for l in range(1, len(w_list)):
            dot_l = (a@w_list[l]) + b_list[l]
            a = vectorized_A(dot_l)
        if a >= 0.5:
            a = 1
        else:
            a = 0
        if a == y:
            correct += 1
    print(f'Number correctly classified: {correct}')
    print(f'Number incorrectly classified: {len(dataset) - correct}')

def in_circle(array):
    if math.sqrt((array[0])**2 + (array[1])**2) < 1:
        return 1
    else:
        return 0


option = sys.argv[1]
start = time.perf_counter()
if option == 'S':
    training_set = [(np.array([[0, 0]]), np.array([[0, 0]])), (np.array([[0, 1]]), np.array([[0, 1]])), (np.array([[1, 0]]), np.array([[0, 1]])), (np.array([[1, 1]]), np.array([[1, 0]]))]
    w_list = [None, np.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]]), np.array([[random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1)]])]
    b_list = [None, np.array([[random.uniform(-1, 1), random.uniform(-1, 1)]]), np.array([[random.uniform(-1, 1), random.uniform(-1, 1)]])]
    sum_train(w_list, b_list, training_set, 7500, 0.8, sigmoid, sigmoid_deriv)
    end = time.perf_counter()
    print(f'Time: {end-start} sec.')
else:
    training_set = []
    with open('10000_pairs.txt') as f:
        for line in f:
            string_points = line.strip().split()
            points = np.array([[float(str_pt) for str_pt in string_points]])
            training_set.append((points, np.array([[in_circle(points[0])]])))
    w_list = [None, np.array([[random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)], [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]]), np.array([[random.uniform(-1, 1)], [random.uniform(-1, 1)], [random.uniform(-1, 1)], [random.uniform(-1, 1)]])]
    b_list = [None, np.array([[random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]]), np.array([random.uniform(-1, 1)])]
    circle_train(w_list, b_list, training_set, 7500, 0.2, sigmoid, sigmoid_deriv)