import sys
import time
import random
import pickle

LENGTH_OF_STRATEGY = 9 # the number of coefficients in one strategy
NUM_POPULATION = 500 # the size of one generation
NUM_TRIALS = 5 # number of trials we take to average to calculate fitness function
NUM_CLONES = 20 # number of clones from one generation to the next
TOURNAMENT_SIZE = 25 # size of the tournament during the selection process
TOURNAMENT_WIN_PROBABILITY = .75 # probability that the best strat wins the tournament
MUTATION_RATE = .3 # probability of mutation
#add more here

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
        final_string += '|'
        for c in sub_list:
            final_string += (' ' + c)
        final_string += ' |'
        final_string += '\n'
    print(final_string)

def get_pieces():
    return list(pieces.keys())

def get_orientations(piece):
    return list(pieces[piece].keys())

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
        return None, 0
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
                return None, 0
            board[row_to_drop][column] = '#'
            row_to_drop -= 1
            current_blocks -= 1
    board, points = clear_rows(board)
    #new_max_heights = update_max_heights(board, my_max_heights)
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

def make_new_board():
    return [[' '] * 10] * 20

def play_game(strategy):
    board = make_new_board()
    max_heights = {i:0 for i in range(10)}
    max_heights = update_max_heights(board, max_heights)
    points = 0
    while board is not None:
        all_boards = list()
        piece = random.choice(get_pieces())
        for piece_orientation in get_orientations(piece):
            for index in range(0, 10-pieces[piece][piece_orientation][1]+1):
                poss_board = [row[:] for row in board]
                poss_board, poss_points_scored = drop_piece(poss_board, pieces[piece][piece_orientation], index, max_heights)
                poss_score = heuristic(poss_board, strategy, poss_points_scored)
                all_boards.append((poss_board, poss_score, poss_points_scored))
        board, heur_score, points_scored = max(all_boards, key=lambda t:t[1])
        if board is not None:
            max_heights = update_max_heights(board, max_heights)
        points += points_scored
        #print_board(board)
    #print(points)
    return points

def play_and_print_game(strategy):
    board = make_new_board()
    max_heights = {i:0 for i in range(10)}
    max_heights = update_max_heights(board, max_heights)
    points = 0
    while board is not None:
        all_boards = list()
        piece = random.choice(get_pieces())
        for piece_orientation in get_orientations(piece):
            for index in range(0, 10-pieces[piece][piece_orientation][1]+1):
                poss_board = [row[:] for row in board]
                poss_board, poss_points_scored = drop_piece(poss_board, pieces[piece][piece_orientation], index, max_heights)
                poss_score = heuristic(poss_board, strategy, poss_points_scored)
                all_boards.append((poss_board, poss_score, poss_points_scored))
        board, heur_score, points_scored = max(all_boards, key=lambda t:t[1])
        if board is not None:
            max_heights = update_max_heights(board, max_heights)
        points += points_scored
        if board is not None:
            print_board(board)
        print(f'Current score: {points}')
    return points

#returns number of holes, number of columns with holes
def get_num_holes(board):
    holes = 0
    cols_with_holes = 0
    for c in range(10):
        found = False
        col_has_hole = False
        for r in range(20):
            if board[r][c] != ' ':
                found = True
            elif found and board[r][c] == ' ':
                holes += 1
                col_has_hole = True
        if col_has_hole:
            cols_with_holes
    return holes, cols_with_holes

def number_of_lines_cleared(poss_points_scored):
    if poss_points_scored == 40:
        return 1
    elif poss_points_scored == 100:
        return 2
    elif poss_points_scored == 300:
        return 3
    else:
        return 4

#returns aggregate height, tallest height, lowest height, avg height, cols_with_no_blocks, bumpiness
def sum_of_heights(board):
    list_of_heights = list()
    for c in range(10):
        found = False
        for r in range(20):
            if board[r][c] != ' ':
                found = True
                list_of_heights.append(20-r)
                break
        if not found:
            list_of_heights.append(0)
    sum_height = sum(list_of_heights)
    avg_height = sum_height / 10
    max_height = max(list_of_heights)
    min_height = min(list_of_heights)
    cols_with_no_blocks = list_of_heights.count(0)
    bumpiness = 0
    for i in range(1, 10):
        bumpiness += abs(list_of_heights[i]-list_of_heights[i-1])
    return sum_height, max_height, min_height, avg_height, cols_with_no_blocks, bumpiness

def heuristic(board, strategy, poss_points_scored):
    if board == None:
        return float('-inf')
    A, B, C, D, E, F, G, H, I = strategy
    heuristic_value = 0
    num_holes, num_cols_with_holes = get_num_holes(board)#returns number of holes, number of columns with holes
    heuristic_value += A * (num_holes)#number of holes in board
    heuristic_value += B * (num_cols_with_holes)#number of columns with holes
    heuristic_value += C * (number_of_lines_cleared(poss_points_scored))#number of lines cleared
    aggregate_height, tallest_height, lowest_height, avg_height, cols_with_no_blocks, bumpiness = sum_of_heights(board) #returns aggregate height, tallest height, lowest height, avg height, cols_with_no_blocks
    heuristic_value += D * (aggregate_height)#aggregate height
    heuristic_value += E * (tallest_height)#highest height
    heuristic_value += F * (tallest_height - lowest_height)#tallest - lowest height
    heuristic_value += G * (avg_height)#average height
    heuristic_value += H * (cols_with_no_blocks)#columns with no blocks
    heuristic_value += I * (bumpiness)#bumpiness (absolute value of differences between columns)
    return heuristic_value

def gen_population():
    population = list()
    for i in range(NUM_POPULATION):
        temp_strat = [random.uniform(-1, 1) for j in range(LENGTH_OF_STRATEGY)]
        temp_fitness = fitness(temp_strat)
        print(f'Strategy number {i} : {temp_fitness}')
        population.append((temp_strat, temp_fitness))
    return population

def fitness(strategy):
    if tuple(strategy) in store_fitness.keys():
       return store_fitness[tuple(strategy)]
    game_scores = []
    for count in range(NUM_TRIALS):
        game_scores.append(play_game(strategy))
    final_fitness = sum(game_scores)/NUM_TRIALS
    store_fitness[tuple(strategy)] = final_fitness
    return final_fitness

def breed(strategy1, strategy2):
    child = [None]*LENGTH_OF_STRATEGY
    num_copies = random.randint(1, LENGTH_OF_STRATEGY-1)
    for copy_index in random.sample([num for num in range(LENGTH_OF_STRATEGY)], num_copies):
        child[copy_index] = strategy1[copy_index]
    for index, value in enumerate(child):
        if value == None:
            child[index] = strategy2[index]
    return tuple(child)

def mutate(strategy):
    mutate_index = random.randint(0, LENGTH_OF_STRATEGY-1)
    strategy = list(strategy)
    strategy[mutate_index] = random.uniform(-1, 1)
    return tuple(strategy)

def avg_fitness_population(population):
    return sum([item[1] for item in population])/NUM_POPULATION

def sort_fitness(strategy):
    if tuple(strategy) in store_fitness.keys():
        return store_fitness[tuple(strategy)]
    else:
        fitness_score = fitness(strategy)
        store_fitness[tuple(strategy)] = fitness_score
        return fitness_score

#given sorted population
def selection(population):
    old_population = [(tuple(strategy[0]), strategy[1]) for strategy in population]
    new_gen = set()
    for i in range(NUM_CLONES):
        new_gen.add((old_population[i][0], old_population[i][1]))
    while len(new_gen) < NUM_POPULATION:
        #print(len(new_gen))
        #print('here')

        all_participants = random.sample(old_population, 2*TOURNAMENT_SIZE)
        tourney1 = all_participants[:len(all_participants)//2]#split all participants into two tourneys
        tourney2 = all_participants[len(all_participants)//2:]
       # print('okok')
        tourney1.sort(key=lambda t:t[1], reverse=True)#sort both of them by fitness
        tourney2.sort(key=lambda t:t[1], reverse=True)
        #print('sorted')
        winner1, winner2 = run_tournament(tourney1, tourney2)#run the tournament and get winners
        parents = [winner1, winner2]
        random.shuffle(parents)#randomize which parent is which winner
        parent1, parent2 = parents[0], parents[1]
        child = breed(parent1, parent2)#breed the parents and get the child
        if random.random() < MUTATION_RATE:#mutate maybe
            child = mutate(child)
        temp_fitness = fitness(child)
        print(f'Strategy number {len(new_gen)} : {temp_fitness}')
        new_gen.add((child, temp_fitness))#add to new generation
    
    return list(new_gen)#return list form of new generation
    #return [(list(strat), fitness(list(strat))) for strat in new_gen]


def run_tournament(sorted_tourney1, sorted_tourney2):
    for count, strategy in enumerate(sorted_tourney1):
        if random.random() <= TOURNAMENT_WIN_PROBABILITY:
            winner1 = strategy[0]
            break
        if count == len(sorted_tourney1)-1:
            winner1 = strategy[0]
            break
    for count, strategy in enumerate(sorted_tourney2):
        if random.random() <= TOURNAMENT_WIN_PROBABILITY:
            winner2 = strategy[0]
            break
        if count == len(sorted_tourney2)-1:
            winner2 = strategy[0]
            break
    return winner1, winner2

def begin_tetris():
    new_or_load = input('(N)ew process, or (L)oad a saved process? ')
    if new_or_load == 'N':
        population = gen_population()#[(strat, fitness(strat)) for strat in gen_population()]
        generation = 0
        average_fitness = avg_fitness_population(population)
        print(f'Average: {average_fitness}')
        print(f'Generation: {generation}')
        population.sort(key=lambda t:t[1], reverse=True)
        best_strat = population[0]
        print(f'Best strategy so far: {best_strat[0]}, fitness: {best_strat[1]}')
        while True:
            next_step = input('(P)lay a game with current best strategy, (S)ave current process, or (C)ontinue? ')
            if next_step == 'C':
                population = selection(population)
                generation += 1
                average_fitness = avg_fitness_population(population)
                print(f'Average: {average_fitness}')
                print(f'Generation: {generation}')
                population.sort(key=lambda t:t[1], reverse=True)
                best_strat = population[0]
                print(f'Best strategy so far: {best_strat[0]}, fitness: {best_strat[1]}')
            elif next_step == 'P':
                play_and_print_game(best_strat[0])
            else:
                filename = input('What filename? ')
                outfile = open(filename,'wb')
                pickle.dump(population,outfile)
                pickle.dump(generation,outfile)
                outfile.close()
                return
    elif new_or_load == 'L':
        filename = input('What filename? ')
        infile = open(filename, 'rb')
        population = pickle.load(infile)
        generation = pickle.load(infile)
        infile.close()
        print(f'Generation: {generation}')
        population.sort(key=lambda t:t[1], reverse=True)
        best_strat = population[0]
        print(f'Best strategy so far: {best_strat[0]}, fitness: {best_strat[1]}')
        while True:
            next_step = input('(P)lay a game with current best strategy, (S)ave current process, or (C)ontinue? ')
            if next_step == 'C':
                population = selection(population)
                generation += 1
                average_fitness = avg_fitness_population(population)
                print(f'Average: {average_fitness}')
                print(f'Generation: {generation}')
                population.sort(key=lambda t:t[1], reverse=True)
                best_strat = population[0]
                print(f'Best strategy so far: {best_strat[0]}, fitness: {best_strat[1]}')
            elif next_step == 'P':
                play_and_print_game(best_strat[0])
            else:
                filename = input('What filename? ')
                outfile = open(filename,'wb')
                pickle.dump(population,outfile)
                pickle.dump(generation,outfile)
                outfile.close()
                return
    else:
        print('Invalid letter')
    return

store_fitness = {}
begin_tetris()
#print(breed([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0], [8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0]))
#print(mutate([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]))