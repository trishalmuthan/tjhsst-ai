import sys
import time
import random

#read the contents of the dictionary file into a sorted list and return. Filter out bad stuff
def read_in(filename, min_length):
    dictionary = dict()
    dictionary_set = set()
    with open(filename) as dictionary_file:
        for line in dictionary_file:
            word = line.split()[0].lower()
            if word.isalpha() and len(word) >= min_length:
                for idx in range(len(word)-1):
                    if word[0:idx+1] in dictionary:
                        if word[0:idx+2] not in dictionary[word[0:idx+1]]:
                            dictionary[word[0:idx+1]].append(word[0:idx+2])
                    else:
                        dictionary[word[0:idx+1]] = [word[0:idx+2]]
                dictionary[word] = [None]
    return dictionary

def possibleMoves(word, dictionary):
    possible_moves = list()
    if word == "":
        return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    else:
        for move in dictionary[word]:
            possible_moves.append(move)
    return possible_moves

#return a list of letters that guarantee win
def find_guaranteed_win(dictionary, min_length, starting_word):
    player = len(starting_word) % 2
    if player == 0:
        list_of_letters = max_move(starting_word, dictionary, player)
    else:
        list_of_letters = min_move(starting_word, dictionary, player)
    uppercase_letters = [letter.upper() for letter in list_of_letters] 
    return uppercase_letters

def max_move(word, dictionary, player):
    pot_moves = list()
    alpha = float('-inf')
    beta = float('inf')
    for new_word in possibleMoves(word, dictionary):
        return_val = min_step(new_word, alpha, beta, dictionary, player)
        pot_moves.append((new_word, return_val))
    best_moves = list()
    for new_word, return_val in pot_moves:
        if return_val == 1:
            best_moves.append(new_word[-1])
    return best_moves

def min_step(word, alpha, beta, dictionary, player):
    if None in dictionary[word] and len(word) >= min_length:
        if len(word) % 2 == 1:
            return -1
        else:
            return 1
    results = list()
    for new_word in possibleMoves(word, dictionary):
        return_val = max_step(new_word, alpha, beta, dictionary, player)
        results.append(return_val)
    return min(results)

def min_move(word, dictionary, player):
    pot_moves = list()
    alpha = float('-inf')
    beta = float('inf')
    for new_word in possibleMoves(word, dictionary):
        return_val = max_step(new_word, alpha, beta, dictionary, player)
        pot_moves.append((new_word, return_val))
    best_moves = list()
    for new_word, return_val in pot_moves:
        if return_val == -1:
            best_moves.append(new_word[-1])
    return best_moves

def max_step(word, alpha, beta, dictionary, player):
    if None in dictionary[word] and len(word) >= min_length:
        if len(word) % 2 == 1:
            return -1
        else:
            return 1
    results = list()
    for new_word in possibleMoves(word, dictionary):
        return_val = min_step(new_word, alpha, beta, dictionary, player)
        results.append(return_val)
    return max(results)

def start_in_dictionary(word, dictionary_set):
    for item in dictionary_set:
        if len(word) < len(item):
            if item[:len(word)] == word:
                return True
    return False


#read and store command-line arguments
filename = sys.argv[1]
min_length = int(sys.argv[2])
if len(sys.argv) > 3:
    starting_word = sys.argv[3].lower()
else:
    starting_word = ""

#read in and create dictionary
dictionary = read_in(filename, min_length)
max_length = len(max(dictionary, key = len)) 
#get list of letters that guarantee win
guaranteed_win_letters = find_guaranteed_win(dictionary, min_length, starting_word)
#print out information
if len(guaranteed_win_letters) > 0:
    print(f'Next player can guarantee victory by playing any of these letters: {guaranteed_win_letters}')
else:
    print('Next player will lose!')