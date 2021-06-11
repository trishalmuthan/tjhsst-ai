import sys
import time

def one_letter_apart(str1,str2):
    if sum ( str1[i] != str2[i] for i in range(len(str1)) ) == 1: return True

def get_children(word):
    return words[word]

def BFS(start, goal):
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
        if v == goal:
            return v, came_from, count
        for child in get_children(v):
            if child not in visited:
                fringe.append(child)
                visited.add(child)
                came_from[child] = v
    return None, None, None

def construct_path(came_from, current):
    boards = list()
    while current in came_from:
        boards.append(current)
        current = came_from[current]
    boards.reverse()
    for board in boards:
        print(board)

words = dict()
with open(sys.argv[1]) as f1:
    start = time.perf_counter()
    for line in f1:
        currentWord = line.strip()
        words[currentWord] = list()
        for key in words:
            if one_letter_apart(key, currentWord):
                words[key].append(currentWord)
                words[currentWord].append(key)
    end = time.perf_counter()
    print(f"Time to create the data structure was: {end - start} seconds")
    print(f"There are {len(words)} words in this dict.")
    print()

with open(sys.argv[2]) as f2:
    begin = time.perf_counter()
    for count, line in enumerate(f2):
        print(f"Line: {count}")
        puzzle = line.split()
        start = puzzle[0]
        goal = puzzle[1]
        goal, came_from, count = BFS(start, goal)
        if goal != None:
            print(f"Length is: {count+1}")
            construct_path(came_from, goal)
        else:
            print("No Solution!")
        print()
    end = time.perf_counter()
    print(f"Time to solve all of these puzzles was: {end - begin} seconds")
