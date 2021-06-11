import sys
import time
import random


def find_next_move(board, player, depth):
    # Based on whether player is x or o, start an appropriate version of minimax
    # that is depth-limited to "depth".  Return the best available move.
    if player == 'x':
        ai_index_move = max_move(board, depth)
    else:
        ai_index_move = min_move(board, depth)
    return ai_index_move

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

#helper for possibleMoves
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

#scoring heuristic
def score_board(board):
    final_score = 0
    num_open_spaces = board.count('.')
    num_black_moves = len(possibleMoves(board, 'x'))
    num_white_moves = len(possibleMoves(board, 'o'))

    #game over
    if num_open_spaces == 0 or (num_black_moves == 0 and num_white_moves == 0):
        if board.count('x') > board.count('o'):
            final_score += 10000000
            final_score += (board.count('x') - board.count('o'))
            return final_score
        else:
            final_score -= 10000000
            final_score += (board.count('x') - board.count('o'))
            return final_score

    #mobility
    base_mobility_score = num_black_moves - num_white_moves
    #CHANGES: if early game, weight mobility more
    if num_open_spaces > 32:
        weighted_mobility_score = base_mobility_score * 3
    else:
        weighted_mobility_score = base_mobility_score * 2

    #corners
    base_corner_score = 0
    if board[0] == 'x':
        base_corner_score += 35
    elif board[0] == 'o':
        base_corner_score -= 35
    if board[7] == 'x':
        base_corner_score += 35
    elif board[7] == 'o':
        base_corner_score -= 35
    if board[56] == 'x':
        base_corner_score += 35
    elif board[56] == 'o':
        base_corner_score -= 35
    if board[63] == 'x':
        base_corner_score += 35
    elif board[63] == 'o':
        base_corner_score -= 35
    weighted_corner_score = base_corner_score * 4.5
    
    #more tokens in endgame
    base_numtoken_score = 0
    #CHANGES: if end game, incorporate number of tokens into heuristic
    if num_open_spaces < 28:
        base_numtoken_score += (board.count('x') * 6)
        base_numtoken_score -= (board.count('o') * 6)

    #next to corner
    base_nexttoc_score = 0
    if board[0] == '.':
        if board[1] == 'x' or board[8] == 'x' or board[9] == 'x':
            base_nexttoc_score -= 10
        if board[1] == 'o' or board[8] == 'o' or board[9] == 'o':
            base_nexttoc_score += 10
        if board[6] == 'x' or board[14] == 'x' or board[15] == 'x':
            base_nexttoc_score -= 10
        if board[6] == 'o' or board[14] == 'o' or board[15] == 'o':
            base_nexttoc_score += 10
        if board[48] == 'x' or board[49] == 'x' or board[57] == 'x':
            base_nexttoc_score -= 10
        if board[48] == 'o' or board[49] == 'o' or board[57] == 'o':
            base_nexttoc_score += 10
        if board[54] == 'x' or board[55] == 'x' or board[62] == 'x':
            base_nexttoc_score -= 10
        if board[54] == 'o' or board[55] == 'o' or board[62] == 'o':
            base_nexttoc_score += 10

    final_score += weighted_corner_score
    final_score += weighted_mobility_score
    final_score += base_numtoken_score
    final_score += base_nexttoc_score

    return final_score
        

def max_move(board, depth):
    pot_moves = list()
    alpha = float('-inf')
    beta = float('inf')
    for index in possibleMoves(board, 'x'):
        next_board = move(board, 'x', index)
        return_val = min_step(next_board, alpha, beta, depth-1)
        #PRUNING
        if return_val > alpha:
            alpha = return_val
        pot_moves.append((index, return_val))
    best_move = max(pot_moves, key=lambda x:x[1])
    return best_move[0]

def min_step(board, alpha, beta, depth):
    if depth == 0:
        return score_board(board)
    results = list()
    for index in possibleMoves(board, 'o'):
        next_board = move(board, 'o', index)
        return_val = max_step(next_board, alpha, beta, depth-1)
        #PRUNING
        if return_val < beta:
            beta = return_val
        results.append(return_val)
        if alpha >= beta:
            break
    if len(results) == 0:
        return max_step(board, alpha, beta, depth-1)
    return min(results)

def max_step(board, alpha, beta, depth):
    if depth == 0:
        return score_board(board)
    results = list()
    for index in possibleMoves(board, 'x'):
        next_board = move(board, 'x', index)
        return_val = min_step(next_board, alpha, beta, depth-1)
        #PRUNING
        if return_val > alpha:
            alpha = return_val
        results.append(return_val)
        if alpha >= beta:
            break 
    if len(results) == 0:
        return min_step(board, alpha, beta, depth-1)
    return max(results)

def min_move(board, depth):
    pot_moves = list()
    alpha = float('-inf')
    beta = float('inf')
    for index in possibleMoves(board, 'o'):
        next_board = move(board, 'o', index)
        return_val = max_step(next_board, alpha, beta, depth-1)
        #PRUNING
        if return_val < beta:
            beta = return_val
        pot_moves.append((index, return_val))
    best_move = min(pot_moves, key=lambda x:x[1])
    return best_move[0]

board = sys.argv[1]
player = sys.argv[2]
depth = 1
for count in range(20):
   print(find_next_move(board, player, depth))
   depth += 1


"""class Strategy():
   logging = False  # Optional
   def best_strategy(self, board, player, best_move, still_running):
       depth = 1
       while True:
           print(depth)
           best_move.value = find_next_move(board, player, depth)
           depth += 1"""