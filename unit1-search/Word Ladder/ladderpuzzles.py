import sys
import time

def diff_letters(str1,str2):
    return sum ( str1[i] != str2[i] for i in range(len(str1)) )

def get_children(word):
    return words[word]

def nBFS(start):
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
            fringe.append(None)
            if fringe[0] == None:
                break
            else:
                continue
        count += 1
        for child in get_children(v):
            if child not in visited:
                fringe.append(child)
                visited.add(child)
                came_from[child] = v
    return count


def construct_path(came_from, current):
    boards = list()
    while current in came_from:
        boards.append(current)
        current = came_from[current]
    boards.reverse()
    for board in boards:
        print(board)

words = dict()

with open("words_06_letters.txt") as f1:
    for line in f1:
        currentWord = line.strip()
        words[currentWord] = list()
        for key in words:
            if diff_letters(key, currentWord) == 1:
                words[key].append(currentWord)
                words[currentWord].append(key)

#Part 1
print("Brainteaser 1: ")
print(sum(len(words[key]) == 0 for key in words))

#Part 2
print("Brainteaser 2: ")
sizes = list()
for word in words:
    sizes.append(nBFS(word))
print( max(sizes) )

def BFS3():
    totalVisited = set()
    totalCount = 0
    for word in words:
        if word not in totalVisited:
            clump = list()
            fringe = list()
            visited = set()
            came_from = dict()
            came_from[word] = None
            fringe.append(word)
            fringe.append(None)
            visited.add(word)
            count = 0
            clump.append(word)
            while fringe:
                v = fringe.pop(0)
                if v == None:
                    fringe.append(None)
                    if fringe[0] == None:
                        break
                    else:
                        continue
                count += 1
                for child in get_children(v):
                    if child not in visited:
                        fringe.append(child)
                        visited.add(child)
                        came_from[child] = v
                        totalVisited.add(child)
                        clump.append(child)
            if len(clump) >= 2:
                totalCount += 1
    return totalCount


#Part 3
print("Brainteaser 3: ")
print(BFS3())

def hardestpuzzle(start):
    fringe = list()
    visited = set()
    came_from = dict()
    came_from[start] = None
    fringe.append(start)
    fringe.append(None)
    visited.add(start)
    count = 1
    currentMax = 1
    maxList = list()
    maxList.append(start)
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


#Part 4
print("Brainteaser 4: ")
lister = list()
for word in words:
    maxList, currentMax = hardestpuzzle(word)
    lister.append(currentMax)
print( max(lister) )