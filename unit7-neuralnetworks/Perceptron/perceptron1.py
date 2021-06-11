import sys
import math
import time
import random
import ast

def dec_to_bin(x, bits):
    to_return = format(x, 'b')
    to_return = '0' * (2**bits - len(to_return)) + to_return
    return to_return

def truth_table(bits, n):
    table = dict()
    values = dec_to_bin(n, bits)
    print(values)
    counter = 0
    for i in range(2**bits-1, -1, -1): 
        entry = format(i, 'b')
        entry = '0' * (bits - len(entry)) + entry
        tuple_entry = tuple(list(map(int, entry)))
        table[tuple_entry] = int(values[counter])
        counter += 1
    return table

def pretty_print_tt(table):
    output = ''
    key = list(table.keys())[0]
    for i in range(len(key)):
        output += (str(i+1) + ' ')
    output += '| Out\n'
    output += '------------\n'
    for entry, value in table.items():
        for item in entry:
            output += (str(item) + ' ')
        output += ('|  ' + str(value))
        output += '\n'
    print(output)

def step(num):
    if num > 0:
        return 1
    else:
        return 0

def perceptron(A, w, b, x):
    dot_product = sum(p*q for p,q in zip(w, x))
    inner_value = dot_product + b
    return A(inner_value)

def check(n, w, b):
    table = truth_table(len(w), n)
    pretty_print_tt(table)
    correct = 0
    for entry, value in table.items():
        if perceptron(step, w, b, entry) == value:
            correct += 1
    return correct/len(table.items())


n = int(sys.argv[1])
w = ast.literal_eval(sys.argv[2])
b = float(sys.argv[3])
print(check(n, w, b))