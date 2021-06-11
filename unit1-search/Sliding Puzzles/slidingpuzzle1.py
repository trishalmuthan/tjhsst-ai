import sys
import time

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
    fringe = list()
    visited = set()
    came_from = dict()
    came_from[start] = None
    fringe.append(start)
    fringe.append(None)
    visited.add(start)
    count = 0
    while fringe:
        v = fringe.pop(0)
        if v == None:
            count += 1
            fringe.append(None)
            if fringe[0] == None:
                break
            else:
                continue
        if goal_test(v):
            return v, came_from, count
        for child in get_children(v):
            if child not in visited:
                fringe.append(child)
                visited.add(child)
                came_from[child] = v
    return None

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
puzzles, moves = hardestpuzzle("12345678.")
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
print(f"{moves} moves to complete!")

#Final Solution
"""with open(sys.argv[1]) as f:
    for count, line in enumerate(f):
        lineparts = line.split()
        start = time.perf_counter()
        final, came_from, numMoves = BFS(lineparts[1])
        end = time.perf_counter()
        print(f'Line {count}: {lineparts[1]}, {numMoves} moves found in {end - start} seconds')"""
