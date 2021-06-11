import sys
import math
from collections import deque

def get_outcome(board):
    if board[0] == board[1] == board[2]:
        if board[0] == 'X':
            return 'X' 
        if board[0] == 'O':
            return 'O'     
    if board[3] == board[4] == board[5]:
        if board[3] == 'X':
            return 'X' 
        if board[3] == 'O':
            return 'O'
    if board[6] == board[7] == board[8]:
        if board[6] == 'X':
            return 'X' 
        if board[6] == 'O':
            return 'O'
    
    if board[0] == board[3] == board[6]:
        if board[0] == 'X':
            return 'X' 
        if board[0] == 'O':
            return 'O'
    if board[1] == board[4] == board[7]:
        if board[1] == 'X':
            return 'X' 
        if board[1] == 'O':
            return 'O'
    if board[2] == board[5] == board[8]:
        if board[2] == 'X':
            return 'X' 
        if board[2] == 'O':
            return 'O'

    if board[0] == board[4] == board[8]:
        if board[0] == 'X':
            return 'X' 
        if board[0] == 'O':
            return 'O'
    if board[2] == board[4] == board[6]:
        if board[2] == 'X':
            return 'X' 
        if board[2] == 'O':
            return 'O'
    
    if board.count('.') == 0:
        return 'T'
    
    return False

def terminal(board):
    if board[0] == board[1] == board[2]:
        if board[0] == 'X' or board[0] == 'O':
            return True
    if board[3] == board[4] == board[5]:
        if board[3] == 'X' or board[3] == 'O':
            return True
    if board[6] == board[7] == board[8]:
        if board[6] == 'X' or board[6] == 'O':
            return True
    
    if board[0] == board[3] == board[6]:
        if board[0] == 'X' or board[0] == 'O':
            return True
    if board[1] == board[4] == board[7]:
        if board[1] == 'X' or board[1] == 'O':
            return True
    if board[2] == board[5] == board[8]:
        if board[2] == 'X' or board[2] == 'O':
            return True

    if board[0] == board[4] == board[8]:
        if board[0] == 'X' or board[0] == 'O':
            return True
    if board[2] == board[4] == board[6]:
        if board[2] == 'X' or board[2] == 'O':
            return True
    
    if board.count('.') == 0:
        return True
    
    return False

def get_player(board):
    if board.count('.') % 2 == 1:
        return 'X'
    return 'O'

def potential_moves(board):
    player = get_player(board)
    spaces = list()
    for index, char in enumerate(board):
        if char == '.':
            spaces.append(index)
    moves = list()
    for i in spaces:
        new_board = board[:i] + player + board[i+1:]
        moves.append((i, new_board))
    return moves

def display_board(board):
    for i in range(0, 3):
        print(board[i], end='')
    print('  ', end='')
    for num in range(0, 3):
        print(num, end='')
    print()

    for i in range(3, 6):
        print(board[i], end='')
    print('  ', end='')
    for num in range(3, 6):
        print(num, end='')
    print()

    for i in range(6, 9):
        print(board[i], end='')
    print('  ', end='')
    for num in range(6, 9):
        print(num, end='')
    print()

def max_move(board):
    pot_moves = list()
    for index, next_board in potential_moves(board):
        pot_moves.append((index, next_board, min_step(next_board)))
    for move in pot_moves:
        if move[2] == 0:
            outcome = "tie"
        elif move[2] == 1:
            outcome = "win"
        else:
            outcome = "loss"
        print(f'Moving at {move[0]} results in a {outcome}.')
    print()
    best_move = max(pot_moves, key=lambda x:x[2])
    return best_move[0], best_move[1]

def min_move(board):
    pot_moves = list()
    for index, next_board in potential_moves(board):
        pot_moves.append((index, next_board, max_step(next_board)))
    for move in pot_moves:
        if move[2] == 0:
            outcome = "tie"
        elif move[2] == 1:
            outcome = "loss"
        else:
            outcome = "win"
        print(f'Moving at {move[0]} results in a {outcome}.')
    print()
    best_move = min(pot_moves, key=lambda x:x[2])
    return best_move[0], best_move[1]

def max_step(board):
    if terminal(board):
        outcome = get_outcome(board)
        if outcome == 'X':
            return 1
        elif outcome == 'O':
            return -1
        else:
            return 0
    results = list()
    for index, next_board in potential_moves(board):
        results.append(min_step(next_board))
    return max(results)

def min_step(board):
    if terminal(board):
        outcome = get_outcome(board)
        if outcome == 'X':
            return 1
        elif outcome == 'O':
            return -1
        else:
            return 0
    results = list()
    for index, next_board in potential_moves(board):
        results.append(max_step(next_board))
    return min(results)

def play_tictactoe(initial_board):
    #Check if board is already completed
    if terminal(initial_board):
        outcome = get_outcome(initial_board)
        if outcome == 'T':
            print('This board is already completed. The board shows that there was a tie. :)')
        else:
            print(f'This board is already completed. The board shows that {outcome} is the winner. :)')
        return

    #Get the AI's player and set a variable for who's turn it is
    #If empty
    if initial_board.count('X') == 0:
        ai_player = input("Should I be X or O? ")
        if ai_player == 'X':
            r_player = 'O'
            ai_turn = True
        else:
            r_player = 'X'
            ai_turn = False
        print()
    #If not empty
    else:
        ai_player = get_player(initial_board)
        if ai_player == 'X':
            r_player = 'O'
        else:
            r_player = 'X'
        ai_turn = True

    board = initial_board
    while not terminal(board):
        #If it's the players turn
        if not ai_turn:
            #Print the current board
            print('Current Board:')
            display_board(board)
            print()

            #Find and print all open space
            open_space_string = 'You can move to any of these spaces: '
            spaces = list()
            for index, char in enumerate(board):
                if char == '.':
                    spaces.append(index)
            for space in spaces:
                open_space_string += (str(space)+', ')
            open_space_string = open_space_string[:-2] + '.'
            print(open_space_string)

            #Get player's choice
            player_choice = int(input('Your choice? '))
            print()
            board = board[:player_choice] + r_player + board[player_choice+1:]

            #Set turn to AI
            ai_turn = True

        #If it's the AIs turn
        else:
            #Print the current board
            print('Current Board:')
            display_board(board)
            print()

            #Select and print AI move
            if ai_player == 'X':
                ai_index_move, ai_move = max_move(board)
            else:
                ai_index_move, ai_move = min_move(board)
            board = ai_move
            print(f'I choose space {ai_index_move}')
            print()

            #Set turn to real player
            ai_turn = False
        
    #Someone has won
    #Print the current board
    print('Current Board:')
    display_board(board)
    print()

    #Print who won
    outcome = get_outcome(board)
    if outcome == r_player:
        print('You won! I lost. :(')
    elif outcome == ai_player:
        print('I won! You lost. :)')
    else:
        print('We tied!')
    return

def part2and3():
    def is_tie(board):
        if board[0] == board[1] == board[2]:
            if board[0] == 'X' or board[0] == 'O':
                return False
        if board[3] == board[4] == board[5]:
            if board[3] == 'X' or board[3] == 'O':
                return False
        if board[6] == board[7] == board[8]:
            if board[6] == 'X' or board[6] == 'O':
                return False
        
        if board[0] == board[3] == board[6]:
            if board[0] == 'X' or board[0] == 'O':
                return False
        if board[1] == board[4] == board[7]:
            if board[1] == 'X' or board[1] == 'O':
                return False
        if board[2] == board[5] == board[8]:
            if board[2] == 'X' or board[2] == 'O':
                return False

        if board[0] == board[4] == board[8]:
            if board[0] == 'X' or board[0] == 'O':
                return False
        if board[2] == board[4] == board[6]:
            if board[2] == 'X' or board[2] == 'O':
                return False
        
        if board.count('.') == 0:
            return True
    
        return False
    fringe = deque()
    fringe.append(('.........', 0))
    final_boards = set()
    distinct_final = dict()
    game_count = 0
    while fringe:
        cur_board = fringe.popleft()
        if terminal(cur_board[0]):
            game_count += 1 
            final_boards.add(cur_board)
            continue
        for index, pot_board in potential_moves(cur_board[0]):
            fringe.append((pot_board, cur_board[1]+1))
    for board in final_boards:
        cur_steps = board[1]
        if cur_steps == 9:
            if is_tie(board[0]):
                cur_steps = 'Draw'
        if cur_steps in distinct_final.keys():
            distinct_final[cur_steps] += 1
        else:
            distinct_final[cur_steps] = 1


    print(f'Total games: {game_count}')
    print(f'Total final boards: {len(final_boards)}')
    print('----------')
    for steps, count in distinct_final.items():
        if steps == 'Draw':
            print(f'Draw: {count}')
        elif steps % 2 == 1:
            print(f'X in {steps}: {count}')
        else:
            print(f'O in {steps}: {count}')


#part2and3()
play_tictactoe(sys.argv[1])