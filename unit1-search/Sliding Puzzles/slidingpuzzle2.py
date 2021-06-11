import sys
import time
from collections import deque
import heapq

#Print board to terminal
def print_puzzle(size, board):
    finalBoard = ''
    for i in range(len(board)):
        if i % size == 0 and i != 0:
            finalBoard += "\n"
        finalBoard += board[i]
        finalBoard += " "
    print(finalBoard)

#Return goal position
def find_goal(board):
    return ''.join(sorted(board))[1:] + "."

#Return possible game states after 1 move
def get_children(board):
    size = int(len(board)**0.5)
    boardList = list(board)
    possible = list()
    position = board.find(".")
    #Switch with above
    if position - size >= 0:
        newBoard = boardList[:]
        storeChar = newBoard[position-size]
        newBoard[position-size] = "."
        newBoard[position] = storeChar
        possible.append("".join(newBoard))
    #Switch with below
    if position + size < len(board):
        newBoard = boardList[:]
        storeChar = newBoard[position+size]
        newBoard[position+size] = "."
        newBoard[position] = storeChar
        possible.append("".join(newBoard))
    #Switch with right
    if (position + 1) % size != 0:
        newBoard = boardList[:]
        storeChar = newBoard[position+1]
        newBoard[position+1] = "."
        newBoard[position] = storeChar
        possible.append("".join(newBoard))
    #Switch with left
    if position % size != 0:
        newBoard = boardList[:]
        storeChar = newBoard[position-1]
        newBoard[position-1] = "."
        newBoard[position] = storeChar
        possible.append("".join(newBoard))
    return possible

#Return true if board is in goal state, false otherwise
def goal_test(board):
    if board == find_goal(board):
        return True
    return False

#Return hardest puzzle
def hardestpuzzle(start):
    fringe = list()
    visited = set()
    came_from = dict()
    came_from[start] = None
    fringe.append(start)
    fringe.append(None)
    visited.add(start)
    count = 0
    currentMax = 0
    maxList = list()
    while fringe:
        v = fringe.pop(0)
        if v == None:
            count += 1
            fringe.append(None)
            if fringe[0] == None:
                break
            else:
                if count > currentMax:
                    maxList.clear()
                    currentMax = count
                continue
        maxList.append(v)
        for child in get_children(v):
            if child not in visited:
                fringe.append(child)
                visited.add(child)
                came_from[child] = v
    return maxList, currentMax

#Conduct BFS search, return final state and came_from dictionary which contains path
def BFS(start):
    fringe = deque()
    visited = set()
    came_from = dict()
    came_from[start] = None
    fringe.append((start, 0))
    visited.add(start)
    count = 0
    while fringe:
        v = fringe.popleft()
        if goal_test(v[0]):
            return v[0], came_from, v[1]
        for child in get_children(v[0]):
            if child not in visited:
                fringe.append((child, v[1]+1))
                visited.add(child)
                came_from[child] = v[0]
    return None

#Conduct DFS search, return final state and came_from dictionary which contains path
def DFS(start):
    fringe = deque()
    visited = set()
    came_from = dict()
    came_from[start] = None
    fringe.append((start, 0))
    visited.add(start)
    count = 0
    while fringe:
        v = fringe.pop()
        if goal_test(v[0]):
            return v[0], came_from, v[1]
        for child in get_children(v[0]):
            if child not in visited:
                fringe.append((child, v[1]+1))
                visited.add(child)
                came_from[child] = v[0]
    return None

def kDFS(start_state, k):
    fringe = list()
    startAncestors = set()
    startAncestors.add(start_state)
    fringe.append((start_state, 0, startAncestors))
    while fringe:
        v = fringe.pop()
        if goal_test(v[0]):
            return v
        if v[1] < k:
            for child in get_children(v[0]):
                if child not in v[2]:
                    tempAncestors = v[2].copy()
                    tempAncestors.add(child)
                    fringe.append((child, v[1]+1, tempAncestors))
    return None

def ID_DFS(start_state):
    max_depth = 0
    result = None
    while result == None:
        result = kDFS(start_state, max_depth)
        max_depth += 1
    return result

#Prints entire path
def construct_path(came_from, current):
    boards = list()
    while current in came_from:
        boards.append(current)
        current = came_from[current]
    boards.reverse()
    for board in boards:
        print_puzzle(len(board)**0.5, board)
        print('-------')

def parity_check(board):
    size = int(len(board)**0.5)
    blankIndex = board.find(".")
    newBoard = board[:blankIndex] + board[blankIndex+1:]
    count = 0
    for i in range(len(newBoard)-1):
        for j in range(i+1, len(newBoard)):
            if (newBoard[i]) > (newBoard[j]):
                count += 1
    if size % 2 == 1:
        if count % 2 == 0:
            return True
        else:
            return False
    else:
        row = board.find(".") // size
        if row % 2 == 0:
            if count % 2 == 1:
                return True
            else:
                return False
        else:
            if count % 2 == 0:
                return True
            else:
                return False
    
def taxicab(board):
    distance = 0
    size = int(len(board)**0.5)
    for tile in board:
        if tile != '.':
            curLoc = board.find(tile)
            desLoc = find_goal(board).find(tile)
            distance += (abs(((desLoc // size) - (curLoc // size))) + abs(((desLoc % size) - (curLoc % size))))
    return distance

def astar(start_state):
    closed = set()
    fringe = [(taxicab(start_state), start_state, 0)]
    while fringe:
        v = heapq.heappop(fringe)
        if goal_test(v[1]):
            return v
        if v[1] not in closed:
            closed.add(v[1])
            for child in get_children(v[1]):
                if child not in closed:
                    heapq.heappush(fringe, (v[2]+1+taxicab(child), child, v[2]+1))
    return None



#Part 3
"""with open(sys.argv[1]) as f:
    for line in f:
        lineparts = line.split()
        print('Line 0 Start State: ')
        print_puzzle(int(lineparts[0]), lineparts[1])  
        print('Line 0 Goal State: ')      
        print_puzzle(int(lineparts[0]), find_goal(lineparts[1]))
        print('Line 0 Children: ')
        for board in get_children(lineparts[1]):
            print_puzzle(int(lineparts[0]), board)
            print('-------------')"""

#Part 6
"""puzzles, moves = hardestpuzzle("12345678.")
print("Hardest 3x3 Puzzles: ")
for puzzle in puzzles:
    print("Start")
    print_puzzle((3), puzzle)
    print("Path: ")
    final, came_from, count = BFS(puzzle)
    construct_path(came_from, final)
    print("Done!")
    print('--------')
print("Solution: ")
print_puzzle(3, "12345678.")
print(f"{moves} moves to complete!")"""

#BFS and DFS
"""with open(sys.argv[1]) as f:
    for count, line in enumerate(f):
        lineparts = line.split()
        start = time.perf_counter()
        final, came_from, numMoves = DFS(lineparts[1])
        end = time.perf_counter()
        print(f'Line {count}: {lineparts[1]}, {numMoves} moves found in {end - start} seconds')"""

#In one minute
"""with open(sys.argv[1]) as f:
    start = time.perf_counter()
    for count, line in enumerate(f):
        final, came_from, numMoves = BFS(line.split()[0])
        end = time.perf_counter()
        print(f'Line {count}: {line}, {numMoves} moves found in {end - start} seconds')
        if end - start > 60:
            break"""

#Parity Check
"""with open(sys.argv[1]) as f:
    for count, line in enumerate(f):
        print(parity_check(line.split()[1]))"""

#kDFS and ID-DFS
"""with open(sys.argv[1]) as f:
    for count, line in enumerate(f):
        start = time.perf_counter()
        final, came_from, numMoves = BFS(line.split()[0])
        end = time.perf_counter()
        print(f'Line {count}: {line.split()[0]}, BFS - {numMoves} moves found in {end - start} seconds')
        start = time.perf_counter()
        final, numMoves, ancestors = ID_DFS(line.split()[0])
        end = time.perf_counter()
        print(f'Line {count}: {line.split()[0]}, ID-DFS - {numMoves} moves found in {end - start} seconds')"""

#Taxicab distances
"""with open(sys.argv[1]) as f:
    for count, line in enumerate(f):
        print(f'Line {count}: {taxicab(line.split()[0])}')"""

#Final solution
"""with open(sys.argv[1]) as f:
    for count, line in enumerate(f):
        board = line.split()[1]
        option = line.split()[2]
        start = time.perf_counter()
        if not parity_check(board):
            end = time.perf_counter()
            print(f'Line {count}: {board}, no solution determined in {end - start} seconds')
            continue
        else:
            if option == 'B':
                start = time.perf_counter()
                final, came_from, numMoves = BFS(board)
                end = time.perf_counter()
                print(f'Line {count}: {board}, BFS - {numMoves} moves found in {end - start} seconds')
            if option == 'I':
                start = time.perf_counter()
                final, numMoves, ancestors = ID_DFS(board)
                end = time.perf_counter()
                print(f'Line {count}: {board}, ID-DFS - {numMoves} moves found in {end - start} seconds')
            if option == 'A':
                start = time.perf_counter()
                heuristic, final, numMoves = astar(board)
                end = time.perf_counter()
                print(f'Line {count}: {board}, A* - {numMoves} moves found in {end - start} seconds')
            if option == '!':
                start = time.perf_counter()
                final, came_from, numMoves = BFS(board)
                end = time.perf_counter()
                print(f'Line {count}: {board}, BFS - {numMoves} moves found in {end - start} seconds')
                start = time.perf_counter()
                final, numMoves, ancestors = ID_DFS(board)
                end = time.perf_counter()
                print(f'Line {count}: {board}, ID-DFS - {numMoves} moves found in {end - start} seconds')
                start = time.perf_counter()
                heuristic, final, numMoves = astar(board)
                end = time.perf_counter()
                print(f'Line {count}: {board}, A* - {numMoves} moves found in {end - start} seconds')"""

with open(sys.argv[1]) as f:
    start = time.perf_counter()
    for count, line in enumerate(f):
        currentStart = time.perf_counter()
        heuristic, final, numMoves = astar(line.split()[0])
        end = time.perf_counter()
        print(f'Line {count}: {line}, A* (original) - {numMoves} moves found in {end - currentStart} seconds')