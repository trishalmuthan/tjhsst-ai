from collections import deque

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

#EXPLORE LEVEL 1
def explore1():
    #BFS and make dictionary and set with duplicates
    fringe = deque()
    store = dict()
    duplicates = set()
    board = "12345678."
    fringe.append((board, 0))
    while fringe:
        c = fringe.popleft()
        store[c[0]] = c[1]
        for child in get_children(c[0]):
            if child in store and store[child] == c[1] + 1:
                duplicates.add(child)
                fringe.append((child, c[1] + 1))
            if not child in store:
                store[child]= c[1] + 1
                fringe.append((child, c[1] + 1))
    #Print
    print("Length: \t Total: \t Unique: \t Multiple: ")
    for i in range(0, 32):
        total_solutions = 0
        multiple_solutions = 0
        unique_solutions = 0
        for board, sol_length in store.items():
            if sol_length == i:
                total_solutions += 1
                if board in duplicates:
                    multiple_solutions += 1
                else:
                    unique_solutions += 1
        print(str(i) + "\t\t" + str(total_solutions) + "\t\t" + str(unique_solutions) + "\t\t" + str(multiple_solutions))

explore1()