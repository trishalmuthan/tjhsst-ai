import time
import sys
import random

def goal_test(state):
    if None in state: return False
    length = len(state)
    if len(set(state)) != length: return False
    for i in range(length):
        diag = i - state[i]
        anti = i + state[i]
        for down in range(i+1, length):
            if down - state[down] == diag or down + state[down] == anti:
                return False
    return True

    
def get_next_unassigned_var(state):
    mid = len(state)//2
    up = True
    upRow = mid-1
    down = True
    downRow = mid
    while up or down:
        if up:
            if state[upRow] == None:
                return upRow
            if upRow == 0:
                up = False
            upRow -= 1
        if down:
            if state[downRow] == None:
                return downRow
            if downRow == len(state)-1:
                down = False
            downRow += 1


def get_sorted_values(state, rowNum):
    if rowNum == None:
        return []
    length = len(state)
    allVals = [x for x in range(length)]
    iterateAllVals = allVals.copy()
    for col in iterateAllVals:
        if col in state:
            allVals.remove(col)
        else:
            diag = rowNum - col
            anti = rowNum + col
            for up in range(length):
                if rowNum == up or state[up] == None:
                    continue
                if up-state[up] == diag or up+state[up] == anti:
                    allVals.remove(col)
                    break
    def sorter(elem):
        return abs(elem - length/2)
    allVals.sort(key=sorter, reverse=True)
    return allVals


def csp_backtracking(state):
    if goal_test(state): 
        return state
    rowNum = get_next_unassigned_var(state)
    if rowNum == None:
        return None
    newState = state.copy()
    for val in get_sorted_values(state, rowNum):
        newState[rowNum] = val
        result = csp_backtracking(newState)
        if result is not None:
            return result
    return None


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


def incremental_repair(state):
    conflicts, most_conflicted_queen = board_conflicts(state)
    while conflicts > 0:
        print(f'Modified State: {state}')
        print(f'Num. Conflicts: {conflicts}')
        state = switch_queen(state, most_conflicted_queen)
        conflicts, most_conflicted_queen = board_conflicts(state)
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



#Output
start = time.perf_counter()
SIZE_ONE = 31
SIZE_TWO = 32

print("Backtracking: ")
print('---------')

print(f'Board Size: {SIZE_ONE}')
nqueens_list = [None for n in range(SIZE_ONE)]
final = csp_backtracking(nqueens_list)
print(f'Solved N-Queens State: {final}')
print(f'Verify: {test_solution(final)}')

print()

print(f'Board Size: {SIZE_TWO}')
nqueens_list = [None for n in range(SIZE_TWO)]
final = csp_backtracking(nqueens_list)
print(f'Solved N-Queens State: {final}')
print(f'Verify: {test_solution(final)}')

print()
print("Incremental Repair: ")
print('---------')


print(f'Board Size: {SIZE_ONE}')
nqueens_list = [None for n in range(SIZE_ONE)]
flawed_state = generate_flawed(nqueens_list)
print(f'Flawed State: {flawed_state}')
final = incremental_repair(flawed_state)
print(f'Solved N-Queens State: {final}')
print(f'Verify: {test_solution(final)}')

print()

print(f'Board Size: {SIZE_TWO}')
nqueens_list = [None for n in range(SIZE_TWO)]
flawed_state = generate_flawed(nqueens_list)
print(f'Flawed State: {flawed_state}')
final = incremental_repair(flawed_state)
print(f'Solved N-Queens State: {final}')
print(f'Verify: {test_solution(final)}')


end = time.perf_counter()
print(f'Total Time: {end-start} seconds')
