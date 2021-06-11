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

#NEGAMAX MOVE FUNCTION
def negamax_move(board, player):
    pot_moves = list()#list of potenial moves
    for index, next_board in potential_moves(board):#for every potential move
        pot_moves.append((index, next_board, negamax(next_board, player)))#append to the list of the potential moves the (index of the move, the new board itself, the call to negamax)
    for move in pot_moves: #This part just prints out the "work" of the AI
        if move[2] == 0:
            outcome = "tie"
        elif move[2] == 1:
            outcome = "win"
        else:
            outcome = "loss"
        print(f'Moving at {move[0]} results in a {outcome}.')
    print()
    best_move = max(pot_moves, key=lambda x:x[2])#Find the maximum value in this to find the best move
    return best_move[0], best_move[1]#Return it

#NEGAMAX FUNCTION
def negamax(board, player):
    if terminal(board):#If the board is a terminal state
        outcome = get_outcome(board)#Get the outcome
        if outcome == 'X':#If outcome and player are the same return 1, if not return -1, if tie return 0
            if player == 'X':
                return 1
            else:
                return -1
        elif outcome == 'O':
            if player == 'O':
                return 1
            else:
                return -1
        else:
            return 0
    results = list()#list for results
    for index, next_board in potential_moves(board):#for every potential move
        if player == 'X':#find the token of the next player
            next_player = 'O'
        if player == 'O':
            next_player = 'X'
        results.append(-1 * negamax(next_board, next_player))#to the list append -1 * the call to negamax on the opposite token from the current player
    
    return min(results) #we return the min because we want to return the worst case because the opponent would be playing perfectly

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
                ai_index_move, ai_move = negamax_move(board, 'X')
            else:
                ai_index_move, ai_move = negamax_move(board, 'O')
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


play_tictactoe(sys.argv[1])