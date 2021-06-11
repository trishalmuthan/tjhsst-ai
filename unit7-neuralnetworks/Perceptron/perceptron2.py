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

def check_with_table(table, w, b):
    correct = 0
    for entry, value in table.items():
        if perceptron(step, w, b, entry) == value:
            correct += 1
    return correct/len(table.items())

def train_perceptron(table, weight, bias, learning_rate):
    last_weight = float('inf')
    last_bias = float('inf')
    for epoch in range(100):
        if last_weight == weight and last_bias == bias:
            return weight, bias
        else:
            last_weight = weight
            last_bias = bias
        for x, output in table.items():
            f_star = perceptron(step, weight, bias, x)
            output_diff = output - f_star
            weight = tuple(map(lambda i, j: i + j, weight, tuple([(learning_rate)*(output_diff)*input_value for input_value in x])))
            bias = bias + (output_diff * learning_rate)
    return weight, bias

def find_all_truthtables(bits):
    num_correct = 0
    for n in range(2**(2**bits)):
        table = truth_table(bits, n)
        weight = tuple([0]*bits)
        bias = 0
        trained_weight, trained_bias = train_perceptron(table, weight, bias, 1)
        accuracy = check_with_table(table, trained_weight, trained_bias)
        if accuracy == 1:
            num_correct += 1
    return num_correct

bits = int(sys.argv[1])
n = int(sys.argv[2])
table = truth_table(bits, n)
pretty_print_tt(table)
trained_weight, trained_bias = train_perceptron(table, tuple([0]*bits), 0, 1)
accuracy = check_with_table(table, trained_weight, trained_bias)
print(f'Weight vector: {trained_weight}')
print(f'Bias value: {trained_bias}')
print(f'Accuracy: {accuracy}')
#num_correctly_modeled = find_all_truthtables(bits)
#print(f'{2**(2**bits)} possible functions; {num_correctly_modeled} can be correctly modeled.')