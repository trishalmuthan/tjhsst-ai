import time
import sys

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
        """colRight = state[i]
        colLeft = state[i]
        for up in range(i-1, -1, -1):
            colRight += 1
            colLeft -= 1
            if state[up] == colRight or state[down] == colLeft:
                return False"""
    return True

    
def get_next_unassigned_var(state):
    """for rowNum in range(len(state)):
        if state[rowNum] == None:
            return rowNum"""

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
    """available_columns = list()
    allVals = [x for x in range(len(state))]
    for col in allVals:
        if col not in state:
            available_columns.append(col)
    return available_columns"""

    """if rowNum == None:
        return []
    available_columns = list()
    allVals = [x for x in range(len(state))]
    for row in range(rowNum):
        if state[row] in allVals:
            allVals.remove(state[row])
    iterateAllVals = allVals.copy()
    for col in iterateAllVals:
        colRight = col
        colLeft = col
        for up in range(rowNum-1, -1, -1):
            colRight += 1
            colLeft -= 1
            if state[up] == colRight or state[up] == colLeft:
                allVals.remove(col)
                break
        
        
    return allVals"""
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
print("Part 2:")
print('---------')

SIZE_ONE =31
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
print(f'Time: {end-start} sec')