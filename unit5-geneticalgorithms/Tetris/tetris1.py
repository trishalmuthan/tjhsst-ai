import sys
import time
import random

pieces = {
    'I' : {
        0: (1, 4, [0, 0, 0, 0], [1, 1, 1, 1]),
        1: (4, 1, [0], [4])
    },
    'O' : {
        0: (2, 2, [0, 0], [2, 2])
    },
    'T' : {
        0: (2, 3, [0, 0, 0], [1, 2, 1]),
        1: (3, 2, [0, -1], [3, 1]),
        2: (2, 3, [0, 1, 0], [1, 2, 1]),
        3: (3, 2, [0, 1], [1, 3])
    },
    'S' : {
        0: (2, 3, [0, 0, -1], [1, 2, 1]),
        1: (3, 2, [0, 1], [2, 2])    
    },
    'Z' : {
        0: (2, 3, [0, 1, 1], [1, 2, 1]),
        1: (3, 2, [0, -1], [2, 2])
    },
    'J' : {
        0: (2, 3, [0, 0, 0], [2, 1, 1]),
        1: (3, 2, [0, -2], [3, 1]),
        2: (2, 3, [0, 0, 1], [1, 1, 2]),
        3: (3, 2, [0, 0], [1, 3])
    },
    'L' : {
        0: (2, 3, [0, 0, 0], [1, 1, 2]),
        1: (3, 2, [0, 0], [3, 1]),
        2: (2, 3, [0, -1, -1], [2, 1, 1]),
        3: (3, 2, [0, 2], [1, 3])
    }
}

def convert_to_2dlist(initial_board):
    final_list = []
    for count, char in enumerate(initial_board):
        if count % 10 == 0:
            sub = initial_board[count:count+10]
            lst = []
            for j in sub:
                lst.append(j)
            final_list.append(lst)
    return final_list

def convert_to_string(board):
    final_string = ''
    for sub_list in board:
        for c in sub_list:
            final_string += c
    return final_string

def print_board(board):
    final_string = ''
    for sub_list in board:
        for c in sub_list:
            final_string += c
        final_string += '\n'
    print(final_string)

def get_pieces():
    return pieces.keys()

def get_orientations(piece):
    return pieces[piece].keys()

def clear_rows(board):
    num_cleared_rows = 0
    new_board = [row[:] for row in board]
    for row in range(len(board)):
        if len(set(board[row])) == 1 and board[row][0] == '#':
            new_board.pop(row)
            new_board.insert(0, [' ']*10)
            num_cleared_rows += 1
    total_points = 0
    if num_cleared_rows == 0:
        total_points = 0
    if num_cleared_rows == 1:
        total_points = 40
    if num_cleared_rows == 2:
        total_points = 100
    if num_cleared_rows == 3:
        total_points = 300
    if num_cleared_rows == 4:
        total_points = 1200
    return new_board, total_points

def drop_piece(board, piece_info, index, my_max_heights):
    height = piece_info[0]
    width = piece_info[1]
    piece_displacements = piece_info[2]
    num_blocks = piece_info[3]
    #check if width is out of bounds
    if index+width > 10:
        return None, None
    #find column to drop in
    column_displacements = []
    columns_to_drop = list()
    for c in range(index, index+width):
        columns_to_drop.append(c)
        column_displacements.append((c, my_max_heights[index]-my_max_heights[c]))
    displacements = list()
    for count, (column, board_value) in enumerate(column_displacements):
        displacements.append((column, board_value-piece_displacements[count], count))
    column_to_drop, value, count_in_list = min(displacements, key=lambda t:t[1])
    initial_row_to_drop = 20-my_max_heights[column_to_drop]-1
    new_piece_displacements = [piece_displacements[i] - piece_displacements[count_in_list] for i in range(width)]
    for count, column in enumerate(columns_to_drop):
        row_to_drop = initial_row_to_drop + new_piece_displacements[count]
        current_blocks = num_blocks[count]
        while current_blocks > 0:
            if row_to_drop < 0:
                return None, None
            board[row_to_drop][column] = '#'
            row_to_drop -= 1
            current_blocks -= 1
    board, points = clear_rows(board)
    new_max_heights = update_max_heights(board, my_max_heights)
    return board, points

def update_max_heights(board, max_heights):
    new_max_heights = {x: max_heights[x] for x in max_heights}
    for c in range(10):
        found = False
        for r in range(20):
            if board[r][c] != ' ':
                new_max_heights[c] = 20-r
                found = True
                break
        if found:
            continue
        new_max_heights[c] = 0
    return new_max_heights

def place_all_pieces(board, max_heights):
    final_boards = list()
    for piece in get_pieces():
        for piece_orientation in get_orientations(piece):
            for index in range(0, 10-pieces[piece][piece_orientation][1]+1):
                new_board = [row[:] for row in board]
                new_board, points = drop_piece(new_board, pieces[piece][piece_orientation], index, max_heights)
                final_boards.append(new_board)
    return final_boards

def create_file(final_boards):
    f = open('tetrisout.txt', 'w')
    for board in final_boards:
        if board is None:
            f.write('GAME OVER\n')
        else:
            f.write(convert_to_string(board)+'\n')
    f.close()

initial_board = list(sys.argv[1])
board = convert_to_2dlist(initial_board)
max_heights = {i:0 for i in range(10)}
max_heights = update_max_heights(board, max_heights)
final_boards = place_all_pieces(board, max_heights)
create_file(final_boards)
