import sys
import time
import random

def num_conflicts(state, row):
    conflicts = state.count(state[row]) - 1
    diag = row - state[row]
    anti = row + state[row]
    for down in range(len(state)):
        if down == row or state[down] == None:
            continue
        if down - state[down] == diag or down + state[down] == anti:
            conflicts += 1
    return conflicts

#Return total conflicts, row with most conflicts
def board_conflicts(state):
    total_conflicts = 0
    max_conflicts = 0
    max_row = 0 #WATCH THIS
    tie = False
    tied = set()
    for row in range(len(state)):
        store = num_conflicts(state, row)
        total_conflicts += store
        if store > max_conflicts:
            max_conflicts = store
            max_row = row
            tied.clear()
            tie = False
        elif store == max_conflicts:
            tie = True
            tied.add(max_row)
            tied.add(row)
    if tie:
        choice = random.sample(tuple(tied), 1)[0]
        return total_conflicts, choice
    else:
        return total_conflicts, max_row

def incremental_repair(state):
    conflicts, most_conflicted_queen = board_conflicts(state)
    while conflicts > 0:
        print(state)
        print(conflicts)
        print(most_conflicted_queen)
        state = switch_queen(state, most_conflicted_queen)
        conflicts, most_conflicted_queen = board_conflicts(state)
    return state

def switch_queen(state, most_conflicted_queen):
    min_conflicts = num_conflicts(state, most_conflicted_queen)
    min_col = state[most_conflicted_queen]
    og_col = state[most_conflicted_queen]
    tie = False
    tied = set()
    for col in range(len(state)):
        if col != og_col:
            state[most_conflicted_queen] = col
            conflicts = num_conflicts(state, most_conflicted_queen)
            if conflicts < min_conflicts:
                min_col = col
                min_conflicts = conflicts
                tied.clear()
                tie = False
            elif conflicts == min_conflicts:
                tie = True
                tied.add(min_col)
                tied.add(col)
    if tie:
        choice = random.sample(tuple(tied), 1)[0]
        state[most_conflicted_queen] = choice
        return state
    else:
        state[most_conflicted_queen] = min_col
        return state

def generate_flawed(state):
    for row in range(len(state)):
        min_col = 0
        state[row] = 0
        min_conflicts = num_conflicts(state, row)
        for col in range(len(state)):
            state[row] = col
            conflicts = num_conflicts(state, row)
            if conflicts < min_conflicts:
                min_col = col
                min_conflicts = conflicts
        state[row] = min_col
    return state

def test_solution(state):
    for var in range(len(state)):
        left = state[var]
        middle = state[var]
        right = state[var]
        for compare in range(var + 1, len(state)):
            left -= 1
            right += 1
            if state[compare] == middle:
                print(var, "middle", compare)
                return False
            if left >= 0 and state[compare] == left:
                print(var, "left", compare)
                return False
            if right < len(state) and state[compare] == right:
                print(var, "right", compare)
                return False
    return True


"""#Output
print("Part 3:")
print('---------')

SIZE_ONE = 31
print(f'Board Size: {SIZE_ONE}')
nqueens_list = [None for n in range(SIZE_ONE)]
start = time.perf_counter()
final = csp_backtracking(nqueens_list)
end = time.perf_counter()
print(f'Solved N-Queens State: {final}')
print(f'Verify: {test_solution(final)}')
print(f'Time: {end-start} sec')

print()

SIZE_TWO = 32
print(f'Board Size: {SIZE_TWO}')
nqueens_list = [None for n in range(SIZE_TWO)]
start = time.perf_counter()
final = csp_backtracking(nqueens_list)
end = time.perf_counter()
print(f'Solved N-Queens State: {final}')
print(f'Verify: {test_solution(final)}')
print(f'Time: {end-start} sec')"""

#print(incremental_repair([9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 2, 30, 31, 1, 4, 29, 26, 8, 5, 14, 18, 25, 19, 17, 10, 24, 20, 11]))
bruh = incremental_repair(generate_flawed([None, None, None, None, None, None,None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]))
print(test_solution(bruh))