import sys
import time
import random

#Return possible moves for player token
def possibleMoves(board, token):
    final_indices = set() #Will store all the indices to be moved to
    opponent_token = get_opponent(token)
    to_check = [index for index, char in enumerate(board) if char == opponent_token] #Will store all the indices of the opposite token because move must be adjacent to one of these
    possible_indices = set()
    for check_index in to_check:
        open_adjacent_indices = get_open_adjacent_spaces(board, check_index)
        for idx in open_adjacent_indices:
            possible_indices.add(idx)
    for index in possible_indices:
        if is_possible_index(board, token, index):
            final_indices.add(index)
    return sorted(list(final_indices))
  
#check if index actually flips tiles
def is_possible_index(board, token, index):
    opponent_token = get_opponent(token)
    #check down
    temp_index = index+8
    ongoing = False
    while temp_index < len(board):#while above bottom
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    return True
        else:#opponent token found
            ongoing = True
            temp_index += 8
    
    #check up
    temp_index = index-8
    ongoing = False
    while temp_index >= 0:#while below top
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    return True
        else:#opponent token found
            ongoing = True
            temp_index -= 8

    #check right
    temp_index = index+1
    ongoing = False
    while temp_index % 8 != 0:#while left of right
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    return True
        else:#opponent token found
            ongoing = True
            temp_index += 1

    #check left
    temp_index = index-1
    ongoing = False
    while (temp_index+1) % 8 != 0:#while right of left
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    return True
        else:#opponent token found
            ongoing = True
            temp_index -= 1

    #check left-down diagonal
    temp_index = index+7
    ongoing = False
    while (temp_index+1) % 8 != 0 and temp_index < len(board):#while right of left and above bottom
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    return True
        else:#opponent token found
            ongoing = True
            temp_index += 7

    #check right-down diagonal
    temp_index = index+9
    ongoing = False
    while temp_index % 8 != 0 and temp_index < len(board):#while left of right and above bottom
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    return True
        else:#opponent token found
            ongoing = True
            temp_index += 9

    #check left-up diagonal
    temp_index = index-9
    ongoing = False
    while (temp_index+1) % 8 != 0 and temp_index >= 0:#while right of left and above bottom
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    return True
        else:#opponent token found
            ongoing = True
            temp_index -= 9

    #check right-up diagonal
    temp_index = index-7
    ongoing = False
    while temp_index % 8 != 0 and temp_index >= 0:#while left of right and above bottom
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    return True
        else:#opponent token found
            ongoing = True
            temp_index -= 7
        
    return False


def get_open_adjacent_spaces(board, index):
    board_len = int(len(board) ** 0.5)
    adjacent = list()
    up_left = True
    up_right = True
    down_left = True
    down_right = True

    if index+board_len < len(board):#Adjacent down
        if board[index+board_len] == '.':#If empty
            adjacent.append(index+board_len)
    else:#Can't move down
        down_left = False
        down_right = False

    if index-board_len >= 0:#Adjacent Up
        if board[index-board_len] == '.':#If empty
            adjacent.append(index-board_len)
    else:#Can't move up
        up_left = False
        up_right = False

    if (index+1) % board_len != 0:#Adjacent Right
        if board[index+1] == '.': #If empty
            adjacent.append(index+1)
    else:#Can't move right
        up_right = False
        down_right = False

    if index%board_len != 0:#Adjacent Left
        if board[index-1] == '.': #If empty
            adjacent.append(index-1)
    else:#Can't move left
        up_left = False
        down_left = False
    
    if up_left and board[index-board_len-1] == '.':
        adjacent.append(index-board_len-1)
    if up_right and board[index-board_len+1] == '.':
        adjacent.append(index-board_len+1)
    if down_left and board[index+board_len-1] == '.':
        adjacent.append(index+board_len-1)
    if down_right and board[index+board_len+1] == '.':
        adjacent.append(index+board_len+1)
    
    return adjacent
    
#Get the opposite player of token
def get_opponent(token):
    if token == 'x':
        return 'o'
    else:
        return 'x'


def move(board, token, index):
    opponent_token = get_opponent(token)
    final_to_flip = set()
    final_to_flip.add(index)
    
    #check down
    temp_index = index+8
    ongoing = False
    temp_to_flip = set()#to flip in this direction
    while temp_index < len(board):#while above bottom
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    final_to_flip.update(temp_to_flip)#update overall set if there are things to flip
                    break
        else:#opponent token found
            temp_to_flip.add(temp_index)
            ongoing = True
            temp_index += 8
    temp_to_flip.clear()
    
    #check up
    temp_index = index-8
    ongoing = False
    while temp_index >= 0:#while below top
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    final_to_flip.update(temp_to_flip)#update overall set if there are things to flip
                    break
        else:#opponent token found
            temp_to_flip.add(temp_index)
            ongoing = True
            temp_index -= 8
    temp_to_flip.clear()

    #check right
    temp_index = index+1
    ongoing = False
    while temp_index % 8 != 0:#while left of right
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    final_to_flip.update(temp_to_flip)#update overall set if there are things to flip
                    break
        else:#opponent token found
            temp_to_flip.add(temp_index)
            ongoing = True
            temp_index += 1
    temp_to_flip.clear()

    #check left
    temp_index = index-1
    ongoing = False
    while (temp_index+1) % 8 != 0:#while right of left
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    final_to_flip.update(temp_to_flip)#update overall set if there are things to flip
                    break
        else:#opponent token found
            temp_to_flip.add(temp_index)
            ongoing = True
            temp_index -= 1
    temp_to_flip.clear()

    #check left-down diagonal
    temp_index = index+7
    ongoing = False
    while (temp_index+1) % 8 != 0 and temp_index < len(board):#while right of left and above bottom
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    final_to_flip.update(temp_to_flip)#update overall set if there are things to flip
                    break
        else:#opponent token found
            temp_to_flip.add(temp_index)
            ongoing = True
            temp_index += 7
    temp_to_flip.clear()

    #check right-down diagonal
    temp_index = index+9
    ongoing = False
    while temp_index % 8 != 0 and temp_index < len(board):#while left of right and above bottom
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    final_to_flip.update(temp_to_flip)#update overall set if there are things to flip
                    break
        else:#opponent token found
            temp_to_flip.add(temp_index)
            ongoing = True
            temp_index += 9
    temp_to_flip.clear()

    #check left-up diagonal
    temp_index = index-9
    ongoing = False
    while (temp_index+1) % 8 != 0 and temp_index >= 0:#while right of left and above bottom
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    final_to_flip.update(temp_to_flip)#update overall set if there are things to flip
                    break
        else:#opponent token found
            temp_to_flip.add(temp_index)
            ongoing = True
            temp_index -= 9
    temp_to_flip.clear()

    #check right-up diagonal
    temp_index = index-7
    ongoing = False
    while temp_index % 8 != 0 and temp_index >= 0:#while left of right and above bottom
        if board[temp_index] != opponent_token:#if not opponent token
            if not ongoing:#if no row of opponent tokens
                break
            else:#if there is row of opponent tokens
                if board[temp_index] == '.':#if empty space
                    break
                else:#if own token
                    final_to_flip.update(temp_to_flip)#update overall set if there are things to flip
                    break
        else:#opponent token found
            temp_to_flip.add(temp_index)
            ongoing = True
            temp_index -= 7
    temp_to_flip.clear()
        
    for move_index in final_to_flip:
        board = board[:move_index] + token + board[move_index+1:]
    return board


board = sys.argv[1]
cur_token = sys.argv[2]
poss_moves = possibleMoves(board, cur_token)
print(poss_moves)
new_moves = list()
for pot_move in poss_moves:
    new_board = move(board, cur_token, pot_move)
    print(new_board)
    new_moves.append(new_board)