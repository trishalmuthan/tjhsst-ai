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

#Conduct BFS search, return final state and length of path
def BFS(start):
    fringe = deque()
    visited = set()
    came_from = dict()
    fringe.append((start, 0))
    visited.add(start)
    count = 0
    while fringe:
        v = fringe.popleft()
        if goal_test(v[0]):
            return v[0], v[1]
        for child in get_children(v[0]):
            if child not in visited:
                fringe.append((child, v[1]+1))
                visited.add(child)
    return None

#Conduct biBFS search, return final state and length of path
def biBFS(start):
    front = deque()
    back = deque()
    frontvisited = set()
    backvisited = set()
    front.append((start, 0))
    frontvisited.add(start)
    back.append((find_goal(start), 0))
    backvisited.add(find_goal(start))
    while front or back:
        if front:
            vf = front.popleft()
            if vf[0] in backvisited:
                for item in back:
                    if item[0] == vf[0]:
                        return vf[0], vf[1]+item[1]
            for child in get_children(vf[0]):
                if child not in frontvisited:
                    front.append((child, vf[1]+1))
                    frontvisited.add(child)
        if back:
            vb = back.popleft()
            if vb[0] in frontvisited:
                for item in front:
                    if item[0] == vb[0]:
                        return vb[0], vb[1]+item[1]
            for child in get_children(vb[0]):
                if child not in backvisited:
                    back.append((child, vb[1]+1))
                    backvisited.add(child)
    return None

#BFS and DFS
with open(sys.argv[1]) as f:
    for count, line in enumerate(f):
        lineparts = line.split()
        start = time.perf_counter()
        final, numMoves = BFS(lineparts[1])
        end = time.perf_counter()
        print(f'Line {count}: {lineparts[1]}, BFS - {numMoves} moves found in {end - start} seconds')
        start = time.perf_counter()
        final, numMoves = biBFS(lineparts[1])
        end = time.perf_counter()
        print(f'Line {count}: {lineparts[1]}, BiBFS - {numMoves} moves found in {end - start} seconds')


