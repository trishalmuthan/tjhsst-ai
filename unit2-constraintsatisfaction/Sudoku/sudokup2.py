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
            
def get_sorted_values(board_state, var):
    return list(board_state[var])

def create_board_state(state, neighbor_dict, symbol_set):
    board_state = dict()
    for i in range(len(state)):
        if state[i] == '.':
            new_symbol_set = symbol_set.copy()
            board_state[i] = new_symbol_set
        else:
            board_state[i] = set()
            board_state[i].add(state[i])
    return board_state


def forward_looking(board_state, neighbor_dict):
    solved_list = list()
    for index, value_set in board_state.items():
        if len(value_set) == 1:
            solved_list.append(index)
    while solved_list:
        cur_index = solved_list.pop()
        cur_value_set = board_state[cur_index]
        for neighbor_index in neighbor_dict[cur_index]:
            store_len = len(board_state[neighbor_index])
            new_set = board_state[neighbor_index] - cur_value_set
            if store_len != len(new_set):
                if len(new_set) == 0:
                    return None
                elif len(new_set) == 1:
                    solved_list.append(neighbor_index)
                    board_state[neighbor_index] = new_set
                else:
                    board_state[neighbor_index] = new_set
    return board_state

def forward_looking_after_cp(board_state, neighbor_dict, solved_list):
    while solved_list:
        cur_index = solved_list.pop()
        cur_value_set = board_state[cur_index]
        for neighbor_index in neighbor_dict[cur_index]:
            store_len = len(board_state[neighbor_index])
            new_set = board_state[neighbor_index] - cur_value_set
            if store_len != len(new_set):
                if len(new_set) == 0:
                    return None
                elif len(new_set) == 1:
                    solved_list.append(neighbor_index)
                    board_state[neighbor_index] = new_set
                else:
                    board_state[neighbor_index] = new_set
    return board_state

def goal_test(board):
    for index, value_set in board.items():
        if len(value_set) != 1:
            return False
    return True

def get_most_constrained_var(board):
    min_var = None
    min_len = float('inf')
    for index, value_set in board.items():
        if len(value_set) > 1 and len(value_set) < min_len:
            min_var = index
            min_len = len(value_set)
    if min_len > 1:
        return min_var
    else:
        return None
    

def assign(board, var, val):
    new_dict = {k:v for k, v in board.items()}  
    new_dict[var] = {val}
    return new_dict

def csp_backtracking_with_forward_looking(board, neighbor_dict, constraint_list, symbol_set):
    if goal_test(board): 
        return board
    var = get_most_constrained_var(board)
    if var == None:
        return None
    for val in get_sorted_values(board, var):
        new_board = assign(board, var, val)
        checked_board = forward_looking(new_board, neighbor_dict)
        checked_board, solved_list = constraint_propagation(constraint_list, checked_board, symbol_set)
        while (checked_board is not None) and solved_list:
            checked_board = forward_looking_after_cp(checked_board, neighbor_dict, solved_list)
            checked_board, solved_list = constraint_propagation(constraint_list, checked_board, symbol_set)
        if checked_board is not None:
            result = csp_backtracking_with_forward_looking(checked_board, neighbor_dict, constraint_list, symbol_set)
            if result is not None:
                return result
    return None

def constraint_propagation(constraint_list, board_state, symbol_set):
    if board_state == None:
        return None, None
    solved_list = list()
    for constraint_set in constraint_list:
        for value in symbol_set:
            contains_value = list()
            for index in constraint_set:
                if value in board_state[index]:
                    contains_value.append(index)
            if len(contains_value) == 1:
                if len(board_state[contains_value[0]]) != 1:
                    board_state[contains_value[0]] = {value}
                    solved_list.append(contains_value[0])
            elif len(contains_value) == 0:
                return None, None
    return board_state, solved_list
    
def checkSum(board_state, N):
    count = 0
    for key, value in board_state.items():
        count += ord(list(value)[0])
    count -= 48*(N**2)
    print(count)

def print_board(board_state, N):
    board_string = ""
    for i in range(N**2):
        board_string += list(board_state[i])[0]
    print(board_string)

with open(sys.argv[1]) as f:
    for count, line in enumerate(f):
        state = line.split()[0]
        #state = "..............3.85..1.2.......5.7.....4...1...9.......5......73..2.1........4...9"
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

        board_state = create_board_state(state, neighbor_dict, symbol_set)
        new_board_state = forward_looking(board_state, neighbor_dict)
        new_board_state, solved_list = constraint_propagation(constraint_list, new_board_state, symbol_set)
        while solved_list:
            new_board_state = forward_looking_after_cp(new_board_state, neighbor_dict, solved_list)
            new_board_state, solved_list = constraint_propagation(constraint_list, new_board_state, symbol_set) 
        final_board = csp_backtracking_with_forward_looking(new_board_state, neighbor_dict, constraint_list, symbol_set)
        print(count)
        print_board(final_board, N)