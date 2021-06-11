import sys
import time
import math

def count_symbols(state, symbol_set):
    symbol_count = dict()
    for char in symbol_set:
        symbol_count[char] = state.count(char)
    for key, value in symbol_count.items():
        print(f'{key} : {value}')
        

def print_puzzle(board, size, subblock_height, subblock_width):
    finalBoard = '|'
    for i in range(len(board)):
        if i % size == 0 and i != 0:
            finalBoard += "\n"
        if i % subblock_width == 0 and i != 0:
            if i % (subblock_height*size) == 0:
                pass
            else:
                finalBoard += "|"
        if i % (subblock_height*size) == 0 and i != 0:
            finalBoard += "-" * ((size*2) + subblock_height)
            finalBoard += "\n|"
        finalBoard += board[i]
        finalBoard += " "
    print(finalBoard)

def get_next_unassigned_var(state):
    index = state.find('.')
    if index == -1:
        return None
    return index

def get_sorted_values(state, index, neighbor_dict, symbol_set):
    neighbor_set = neighbor_dict[index]
    values = list() 
    for symbol in symbol_set:
        found = False
        for neighbor in neighbor_set:
            if state[neighbor] == symbol:
                found = True
        if not found:
            values.append(symbol)
    if len(values) == 0:
        return []
    else:
        values.sort()
        return values

def goal_test(state):
    if state.find('.') == -1:
        return True
    return False

def csp_backtracking(state, neighbor_dict, symbol_set):
    if goal_test(state): 
        return state
    rowNum = get_next_unassigned_var(state)
    if rowNum == None:
        return None
    newState = state[:]
    for val in get_sorted_values(state, rowNum, neighbor_dict, symbol_set):
        newState = newState[:rowNum]+val+newState[rowNum+1:]
        result = csp_backtracking(newState, neighbor_dict, symbol_set)
        if result is not None:
            return result
    return None
                

with open(sys.argv[1]) as f:
    for count, line in enumerate(f):
        state = line.split()[0]
        #Find N
        N = int(len(state) ** 0.5)

        #Find sublock_width
        width = int(math.ceil(N ** 0.5))
        while N % width != 0:
            width += 1
        subblock_width = width

        #Find subblock_height
        height = int(math.floor(N ** 0.5))
        while N % height != 0:
            height -= 1
        subblock_height = height

        #Create symbol_set
        symbol_set = set()
        if N > 9:
            for num in range(1, 10):
                symbol_set.add(str(num))
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for num2 in range(N-9):
                symbol_set.add(letters[num2])
        else:
            for num in range(1, N+1):
                symbol_set.add(str(num))

        constraint_list = list()

        #Rows
        new_set = set()
        for i in range(len(state)):
            if i % N == 0 and i != 0:
                constraint_list.append(new_set)
                new_set = set()
            new_set.add(i)
        constraint_list.append(new_set)

        #Columns
        for i in range(N):
            new_set = set()
            for j in range(i, len(state), N):
                new_set.add(j)
            constraint_list.append(new_set)
        
        #Blocks
        for right in range(0, N, subblock_width):
            for down in range(right, len(state), subblock_height*N):
                new_set = set()
                for rsub in range(down, down+subblock_width):
                    for dsub in range(rsub, rsub+subblock_height*N, N):
                        new_set.add(dsub)
                constraint_list.append(new_set)

        neighbor_dict = dict()
        for index in range(len(state)):
            neighbor_dict[index] = set()
            for constraint_set in constraint_list:
                if index in constraint_set:
                    new_set = constraint_set.copy()
                    new_set.remove(index)
                    neighbor_dict[index].update(new_set)
        
        board = csp_backtracking(state, neighbor_dict, symbol_set)
        print(count)
        print(board)