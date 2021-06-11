import sys
import math
import time
import random
import ast

def step(num):
    if num > 0:
        return 1
    else:
        return 0

def perceptron(A, w, b, x):
    dot_product = sum(p*q for p,q in zip(w, x))
    inner_value = dot_product + b
    return A(inner_value)

#XOR HAPPENS HERE
def network(input_value):
    in1, in2 = input_value
    output3 = perceptron(step, (2, 2), -1, (in1, in2)) #perceptron 3
    output4 = perceptron(step, (-1, -1), 2, (in1, in2)) #perceptron 4
    output5 = perceptron(step, (1, 1), -1, (output3, output4)) #perceptron 5 where output5 is value of outcome of XOR
    return output5

x = ast.literal_eval(sys.argv[1])
output = network(x)
print(output)
