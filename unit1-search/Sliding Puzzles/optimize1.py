#Optimize 1: Trishal Muthan and Aryan Kumawat

import sys
import time
from collections import deque
import heapq

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
        possible.append((position-size, "".join(newBoard), position, storeChar, False))
    #Switch with below
    if position + size < len(board):
        newBoard = boardList[:]
        storeChar = newBoard[position+size]
        newBoard[position+size] = "."
        newBoard[position] = storeChar
        possible.append((position+size, "".join(newBoard), position, storeChar, False))
    #Switch with right
    if (position + 1) % size != 0:
        newBoard = boardList[:]
        storeChar = newBoard[position+1]
        newBoard[position+1] = "."
        newBoard[position] = storeChar
        possible.append((position+1, "".join(newBoard), position, storeChar, True))
    #Switch with left
    if position % size != 0:
        newBoard = boardList[:]
        storeChar = newBoard[position-1]
        newBoard[position-1] = "."
        newBoard[position] = storeChar
        possible.append((position-1, "".join(newBoard), position, storeChar, True))
    return possible

#Return true if board is in goal state, false otherwise
def goal_test(board):
    if board == find_goal(board):
        return True
    return False
    
def incrTaxicab(board, oldPos, newBoard, newPos, char, positions, isHorizontal):
    size = int(len(board)**0.5)
    if isHorizontal:
        if abs(positions[char][1] - newPos%size) < abs(positions[char][1] - oldPos%size):
            return -1
        else:
            return 1
    else:
        if abs(positions[char][0] - newPos//size) < abs(positions[char][0] - oldPos//size):
            return -1
        else:
            return 1

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
    positions = create_pos(find_goal(start_state))
    taxi = taxicab(start_state)
    fringe = [(taxi, start_state, 0, taxi)]
    heapq.heapify(fringe)
    while fringe:
        v = heapq.heappop(fringe)
        if goal_test(v[1]):
            return v
        if v[1] not in closed:
            closed.add(v[1])
            for oldPos, child, newPos, char, isHoriz in get_children(v[1]):
                if child not in closed:
                    newTaxi = incrTaxicab(v[1], oldPos, child, newPos, char, positions, isHoriz)
                    temp = (v[3]+newTaxi+v[2]+1, child, v[2]+1, v[3]+newTaxi)
                    heapq.heappush(fringe, temp)
    return None

def create_pos(start_state):
    size = int(len(start_state)**0.5)
    board = dict()
    count = 0
    for i in range(size):
        for j in range(size):
            board[start_state[count]] = (i, j)
            count += 1
    return board

with open(sys.argv[1]) as f:
    start = time.perf_counter()
    for count, line in enumerate(f):
        currentStart = time.perf_counter()
        heuristic, final, numMoves, taxi = astar(line.split()[0])
        end = time.perf_counter()
        print(f'Line {count}: {line}, A* (original) - {numMoves} moves found in {end - currentStart} seconds')

