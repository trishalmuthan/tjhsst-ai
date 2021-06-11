import sys
from collections import deque 

"""BEGINS BLOCK PLACING SECTION"""

#print out the puzzle
def print_puzzle(board, num_cols):
    final_string = ""
    for index, square in enumerate(board):
        if index % num_cols == 0 and index != 0:
            final_string += "\n"
        final_string += (square + " ")
    print(final_string)

#add seed strings to the board
def add_words_to_board(board, num_cols, extra_words):
    for direction, row, col, legit_word in extra_words:
        coord = (col + (row * num_cols))
        if direction == 'H':
            for letter in legit_word:
                board[coord] = letter
                if letter == '#':
                    symmetrical_index = len(board) - (coord + 1)
                    board[symmetrical_index] = '#'
                coord += 1
        elif direction == 'V':
            for letter in legit_word:
                board[coord] = letter
                if letter == '#':
                    symmetrical_index = len(board) - (coord + 1)
                    board[symmetrical_index] = '#'
                coord += num_cols
    return board

#fill in all open spaces with @ signs
def area_fill(board, num_rows, num_cols, row, col):
    if row < 0 or row >= num_rows or col < 0 or col >= num_cols:
        return board
    coord = (col + (row * num_cols))
    board[coord] = '@'
    if row-1 >= 0 and board[coord-num_cols] != '@' and board[coord-num_cols] != '#':
        board = area_fill(board, num_rows, num_cols, row-1, col)
    if row+1 < num_rows and board[coord+num_cols] != '@' and board[coord+num_cols] != '#':
        board = area_fill(board, num_rows, num_cols, row+1, col)
    if col-1 >= 0 and board[coord-1] != '@' and board[coord-1] != '#':
        board = area_fill(board, num_rows, num_cols, row, col-1)
    if col+1 < num_cols and board[coord+1] != '@' and board[coord+1] != '#':
        board = area_fill(board, num_rows, num_cols, row, col+1)
    return board

#returns true or false if no part of board is cut off
def fully_connected(board, num_rows, num_cols):
    new_board = board.copy()
    index = new_board.index('-')
    area_filled_board = area_fill(new_board, num_rows, num_cols, index//num_cols, index % num_cols)
    if '-' in area_filled_board:
        return False
    else:
        return True

#gets all implied squares for a given index
def get_implied_squares(board, index, num_rows, num_cols):
    #up
    current_index = index
    up_list = list()
    store_list = list()
    block = True
    for i in range(3):
        current_index -= num_cols
        if current_index >= 0:
            if board[current_index] == '#':
                if not block:
                    for item in store_list:
                        up_list.append(item)
                    break
            else:
                store_list.append(current_index)
                block = False
        else:
            if not block:
                for item in store_list:
                    up_list.append(item)
                break
    #down
    current_index = index
    down_list = list()
    store_list = list()
    block = True
    for i in range(3):
        current_index += num_cols
        if current_index < len(board):
            if board[current_index] == '#':
                if not block:
                    for item in store_list:
                        down_list.append(item)
                    break
            else:
                store_list.append(current_index)
                block = False
        else:
            if not block:
                for item in store_list:
                        down_list.append(item)
                break
    #right
    current_index = index
    right_list = list()
    store_list = list()
    the_row = current_index//num_cols
    block = True
    for i in range(3):
        current_index += 1
        if current_index // num_cols == the_row :
            if board[current_index] == '#':
                if not block:
                    for item in store_list:
                        right_list.append(item)
                    break
            else:
                store_list.append(current_index)
                block = False
        else:
            if not block:
                for item in store_list:
                        right_list.append(item)
                break
    #left
    current_index = index
    left_list = list()
    store_list = list()
    block = True
    for i in range(3):
        current_index -= 1
        if current_index // num_cols == the_row :
            if board[current_index] == '#':
                if not block:
                    for item in store_list:
                        left_list.append(item)
                    break
            else:
                store_list.append(current_index)
                block = False
        else:
            if not block:
                for item in store_list:
                        right_list.append(item)
                break
    total_list = list()
    total_list.append(up_list)
    total_list.append(down_list)
    total_list.append(right_list)
    total_list.append(left_list)
    return sum(total_list,[])

#checks if given index has at least length 3 surrounding it
def check_min_length(board, index, num_rows, num_cols):
    #up
    current_index = index
    block = True
    for i in range(3):
        current_index -= num_cols
        if current_index >= 0:
            if board[current_index] == '#':
                if not block:
                    return False
            else:
                block = False
        else:
            if not block:
                return False
    #down
    current_index = index
    block = True
    for i in range(3):
        current_index += num_cols
        if current_index < len(board):
            if board[current_index] == '#':
                if not block:
                    return False
            else:
                block = False
        else:
            if not block:
                return False
    #right
    current_index = index
    the_row = current_index//num_cols
    block = True
    for i in range(3):
        current_index += 1
        if current_index // num_cols == the_row :
            if board[current_index] == '#':
                if not block:
                    return False
            else:
                block = False
        else:
            if not block:
                return False
    #left
    current_index = index
    block = True
    for i in range(3):
        current_index -= 1
        if current_index // num_cols == the_row :
            if board[current_index] == '#':
                if not block:
                    return False
            else:
                block = False
        else:
            if not block:
                return False
    return True
    
#checks if the entire board is at least min length 3
def check_board_min_length_3(board, num_rows, num_cols):
    if len(board) % 2 == 0:
        final_index = int(len(board)/2)
    else:
        final_index = int((len(board)-1)/2)
    for index, square in enumerate(board[:final_index]):
        if square == '#':
            if not check_min_length(board, index, num_rows, num_cols):
                return False
    return True

#finds all implied squares in the board
def find_implied(board, num_rows, num_cols):
    total = list()
    if len(board) % 2 == 0:
        final_index = int(len(board)/2)
    else:
        final_index = int((len(board)-1)/2)
    for index, square in enumerate(board[:final_index]):
        if board[index] == '#':
            total.append(get_implied_squares(board, index, num_rows, num_cols))
    return sum(total,[])

#conducts search to place down all implied squares
def place_implied_squares(board, num_rows, num_cols, cur_blocks, final_blocks):
    implied_squares = deque(find_implied(board, num_rows, num_cols))
    visited = set(implied_squares)
    if len(implied_squares) == 0:
        return board
    while implied_squares:
        new_index = implied_squares.pop()
        if cur_blocks >= final_blocks: #more implied blocks to place but already all blocks have been placed so return None
            return None
        symmetric_index = len(board) - (new_index + 1)
        if board[new_index] == '-' and board[symmetric_index] == '-':
            board[new_index] = "#"
            board[symmetric_index] = '#'
            if symmetric_index == new_index:
                cur_blocks += 1
            else:
                cur_blocks += 2
        for new_square in find_implied(board, num_rows, num_cols):
            if new_square not in visited:
                implied_squares.append(new_square)
                visited.add(new_square)
    if not check_board_min_length_3(board, num_rows, num_cols):#check if at least length 3 all over board
        return None
    return board

#returns (index, symmetrical index, heuristic) for all possible moves in board sorted by the heuristic
def possibleMoves(board, num_rows, num_cols):
    possible_moves = list()
    if len(board) % 2 == 0:
        final_index = int(len(board)/2)
    else:
        final_index = int((len(board)-1)/2)
    for index, square in enumerate(board[:final_index]):
        symmetrical_index = len(board) - (index + 1)
        if square == '-' and board[symmetrical_index] == '-':
            possible_moves.append((index, symmetrical_index, heuristic(board, index, symmetrical_index, num_rows, num_cols)))
    possible_moves = sorted(possible_moves, key=lambda x: x[2])
    return possible_moves

#returns a score for every given board
def heuristic(board, index, symmetrical_index, num_rows, num_cols):
    total_sum = 0
    new_board = board.copy()
    new_board[index] = '#'
    new_board[symmetrical_index] = '#'
    for i in range(0, len(new_board), num_cols):
        empty = False
        for j in range(0, num_cols):
            if new_board[i+j] != '#' and not empty:
                empty = True
                cur_length = 0
            if new_board[i+j] == '#' and empty:
                empty = False
                total_sum += (cur_length**2)
                cur_length = 0
            if empty:
                cur_length += 1
        if empty:
            empty = False
            total_sum += (cur_length**2)
    for i in range(0, num_cols):
        empty = False
        for j in range(0, len(new_board), num_cols):
            if new_board[i+j] != '#' and not empty:
                empty = True
                cur_length = 0
            if new_board[i+j] == '#' and empty:
                empty = False
                total_sum += (cur_length**2)
                cur_length = 0
            if empty:
                cur_length += 1
        if empty:
            empty = False
            total_sum += (cur_length**2)
    return total_sum

#backtracking method to place blocking squares
def place_blocking_squares(board, num_rows, num_cols, cur_blocks, final_blocks, block_placed):
    if cur_blocks == final_blocks:
        if fully_connected(board, num_rows, num_cols): #only goal tests because blocks are placed symmetrically and min_3_length checked in implied block section
            return board
        else:
            return None
    if block_placed and not fully_connected(board, num_rows, num_cols):
        return None
    elif cur_blocks >= final_blocks:
        return None
    for index, symmetrical_index, heuristic in possibleMoves(board, num_rows, num_cols):
        new_board = board.copy()
        new_board[index] = '#'
        new_board[symmetrical_index] = '#'
        new_board = place_implied_squares(new_board, num_rows, num_cols, board.count('#'), final_blocks)
        if new_board is not None:
            result = place_blocking_squares(new_board, num_rows, num_cols, new_board.count('#'), final_blocks, True)
        else:
            result = None
        if result is not None:
            return result
    return None

arg_list = sys.argv
#rows and columns
r_n_c = arg_list[1]
num_rows = int(r_n_c[:r_n_c.index('x')])
num_cols = int(r_n_c[r_n_c.index('x')+1:])
#blocking squares
num_blocking_squares = int(arg_list[2])
#dictionary file
dictionary_file = arg_list[3]
#extra words
extra_words = list()
if len(arg_list) > 4:
    for word in arg_list[4:]:
        direction = word[0].upper()
        row =  int(word[1:word.index('x')])
        start_index = None
        for index, char in enumerate(word):
            if index <= word.index('x'):
                continue
            if not char.isnumeric():
                start_index = index
                break
        col = int(word[word.index('x')+1:start_index])
        legit_word = word[start_index:]
        extra_words.append((direction, row, col, legit_word.upper()))
#create board
board = ["-"] * (num_rows*num_cols)
add_words_to_board(board, num_cols, extra_words)
temp_board = place_implied_squares(board, num_rows, num_cols, board.count('#'), num_blocking_squares)
if num_rows * num_cols == num_blocking_squares:
    final_board = ["#"] * (num_rows*num_cols)
elif num_rows % 2 == 1 and num_cols % 2 == 1 and num_blocking_squares % 2 == 1:
    coord = int((((num_cols - 1)/2) + (((num_rows - 1)/2) * num_cols)))
    board[coord] = '#'
    final_board = place_blocking_squares(temp_board, num_rows, num_cols, board.count('#'), num_blocking_squares, False)
else:
    final_board = place_blocking_squares(temp_board, num_rows, num_cols, board.count('#'), num_blocking_squares, False)
board = final_board
print_puzzle(board, num_cols)

"""BEGINS WORD PLACING SECTION"""

#return list of tuples of all wordspaces on the board
def find_all_wordspaces(board, num_rows, num_cols):
    wordspace_list = list()
    wordspace_indices = dict()
    #horizontal
    for i in range(0, len(board), num_cols):
        empty = False
        for j in range(0, num_cols):
            if board[i+j] != '#' and not empty:
                empty = True
                cur_start_index = i+j
                cur_length = 0
                store_indices = []
            if board[i+j] == '#' and empty:
                empty = False
                cur_stop_index = i+j-1 #THIS IS THE LAST INDEX WHERE THE EMPTY SPACE IS!!!! 
                wordspace_list.append((cur_start_index, cur_stop_index, 'H', cur_length))
                wordspace_indices[(cur_start_index, cur_stop_index, 'H', cur_length)] = store_indices
                cur_length = 0
            if empty:
                cur_length += 1
                store_indices.append(i+j)
        if empty:
            empty = False
            cur_stop_index = i+j
            wordspace_list.append((cur_start_index, cur_stop_index, 'H', cur_length))
            wordspace_indices[(cur_start_index, cur_stop_index, 'H', cur_length)] = store_indices
    #vertical
    for i in range(0, num_cols):
        empty = False
        for j in range(0, len(board), num_cols):
            if board[i+j] != '#' and not empty:
                empty = True
                cur_start_index = i+j
                cur_length = 0
                store_indices = []
            if board[i+j] == '#' and empty:
                empty = False
                cur_stop_index = i+j-num_cols #THIS IS THE LAST INDEX WHERE THE EMPTY SPACE IS!!!! 
                wordspace_list.append((cur_start_index, cur_stop_index, 'V', cur_length))
                wordspace_indices[(cur_start_index, cur_stop_index, 'V', cur_length)] = store_indices
                cur_length = 0
            if empty:
                store_indices.append(i+j)
                cur_length += 1
        if empty:
            empty = False
            cur_stop_index = i+j
            wordspace_list.append((cur_start_index, cur_stop_index, 'V', cur_length))
            wordspace_indices[(cur_start_index, cur_stop_index, 'V', cur_length)] = store_indices
    return wordspace_list, wordspace_indices
            
#return list of words ordered by letter frequency
def order_by_letter_frequency(word):
    score = 0
    for char in word:
        score -= letter_count[char]
    return score

#return the wordspace with the least amount of possibilities:
def most_constrained_wordspace(wordspace_dict):
    cur_min_wordspace = None
    cur_min_length = float('inf')
    for key in wordspace_dict.keys():
        if len(wordspace_dict[key]) < cur_min_length:
             cur_min_length = len(wordspace_dict[key])
             cur_min_wordspace = key
    return cur_min_wordspace

#return list of words that correspond to that wordspace
def possibleWords(wordspace_dict, wordspace):
    return sorted(wordspace_dict[wordspace], key=order_by_letter_frequency)

#update all the words in the dictionary that we affected
def update_other_words(wordspace_dict, wordspace, wordspace_indices, board, num_rows, num_cols):
    word = ''
    if wordspace[2] == 'H':
        for i in range(wordspace[0], wordspace[1]+1):
            word += board[i]
    else:
        for i in range(wordspace[0], wordspace[1]+1, num_cols):
            word += board[i]
    indices_to_check = wordspace_indices[wordspace]
    for new_wordspace, set_of_words in wordspace_dict.items():
        indices = wordspace_indices[new_wordspace]
        if new_wordspace != wordspace:
            wordspace_dict[new_wordspace].discard(word)
        if any(index in indices for index in indices_to_check) and wordspace[2] != new_wordspace[2]:
            common_index = set(indices).intersection(set(indices_to_check)).pop()
            intersect_index = indices.index(common_index) #the index of the other wordspace where it intersects with the current word
            for new_word in list(wordspace_dict[new_wordspace]):
                if new_word[intersect_index] != board[common_index] and board[common_index] != '-':
                    wordspace_dict[new_wordspace].remove(new_word)
    return wordspace_dict
                        
#place a word on the board in a given wordspace            
def place_word(board, wordspace, word, num_rows, num_cols):
    cur_index = 0
    if wordspace[2] == 'H':
        for i in range(wordspace[0], wordspace[1]+1):
            board[i] = word[cur_index]
            cur_index += 1
    else:
        for i in range(wordspace[0], wordspace[1]+1, num_cols):
            board[i] = word[cur_index]
            cur_index += 1

#backtracking method to place words
def place_all_words(board, num_rows, num_cols, wordspace_dict, letter_count):
    if board.count('-') == 0 and not wordspace_dict:
        return board
    for key in wordspace_dict.keys():
        if not wordspace_dict[key]:
            return None
    wordspace = most_constrained_wordspace(wordspace_dict)
    for word in possibleWords(wordspace_dict, wordspace):
        new_board = board.copy()
        place_word(new_board, wordspace, word, num_rows, num_cols)
        new_wordspace_dict = {x: wordspace_dict[x].copy() for x in wordspace_dict}
        new_wordspace_dict.pop(wordspace)
        new_wordspace_dict = update_other_words(new_wordspace_dict, wordspace, wordspace_indices, new_board, num_rows, num_cols)
        result = place_all_words(new_board, num_rows, num_cols, new_wordspace_dict, letter_count)
        if result is not None:
            return result
    return None

#read in file
len_dict = dict() #dict of len:set of words of that length
with open(dictionary_file) as f:
    for count, line in enumerate(f):
        word = line.split()[0]
        if (len(word) > num_rows and len(word) > num_cols) or (len(word) < 3):
            continue
        if len(word) in len_dict.keys():
            len_dict[len(word)].add(word.upper())
        else:
            len_dict[len(word)] = {word.upper()}

letter_count = dict() #dict of letter:count
with open(dictionary_file) as f:
    text = f.read().upper()
    for char in text:
        if char in letter_count.keys():
            letter_count[char] += 1
        else:
            letter_count[char] = 1

wordspaces_list, wordspace_indices = find_all_wordspaces(board, num_rows, num_cols)
wordspace_dict = dict()
for wordspace in wordspaces_list:
    set_of_words = len_dict[wordspace[3]].copy()
    wordspace_dict[wordspace] = set_of_words
for wordspace in wordspaces_list:
    update_other_words(wordspace_dict, wordspace, wordspace_indices, board, num_rows, num_cols)
final_board = place_all_words(board, num_rows, num_cols, wordspace_dict, letter_count)
print_puzzle(final_board, num_cols)