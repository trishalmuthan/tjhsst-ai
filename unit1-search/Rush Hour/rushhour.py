# rush hour
# HELLO hi

board = [
  ['A', 'A', 'A', '0', '0', 'B'],
  ['0', '0', 'C', '0', '0', 'B'],
  ['*', '*', 'C', '0', '0', 'B'],
  ['D', '0', 'C', '0', 'E', 'E'],
  ['D', '0', '0', '0', 'G', '0'],
  ['F', 'F', 'F', '0', 'G', '0']
]

# returns horizontal oriented cars, rowNum, colNum, and length
def getHorizCars(board):
  carsHoriz = []
  for rowNum, row in enumerate(board):
    for colNum in range(len(row)-1):
      if board[rowNum][colNum] == board[rowNum][colNum+1]:
        length = 0
        for storeCol in range(colNum, len(row)):
          if board[rowNum][colNum] == board[rowNum][storeCol]:
            length+=1
          else:
            break
        carsHoriz.append((board[rowNum][colNum], True, rowNum, colNum, length))
  carsHoriz = list(dict.fromkeys(carsHoriz))
  seen = set() 
  finalCarsHoriz = [(a, b, c, d, e) for a, b, c, d, e in carsHoriz 
         if not (a in seen or seen.add(a))] 
  return finalCarsHoriz

# returns vertical oriented cars, rowNum, colNum, and length
def getVertCars(board):
  carsVert = []
  for rowNum in range(len(board)-1):
    for colNum in range(len(board[0])):
      if board[rowNum][colNum] == board[rowNum+1][colNum]:
        length = 0
        for storeRow in range(rowNum, len(board)):
          if board[rowNum][colNum] == board[storeRow][colNum]:
            length+=1
          else:
            break
        carsVert.append((board[rowNum][colNum], False, rowNum, colNum, length))
  carsVert = list(dict.fromkeys(carsVert))
  seen = set() 
  finalCarsVert = [(a, b, c, d, e) for a, b, c, d, e in carsVert 
         if not (a in seen or seen.add(a))] 
  return finalCarsVert

#print(getVertCars(board))
#print(getHorizCars(board))

"""
pseudocode:
for every car in horizCars:
  attempt movs to the left until you can't any more
  add each state that was moved at least 1 move left to children
  attempt moves to the right until you can't any more
  add each state that was moved at least 1 move to the right to children
  
for every car in vertCars:
  
"""


def get_children(board):
    verticalCars = getVertCars(board)
    horizCars = getHorizCars(board)

    children = []


    for car in horizCars:
        # returns first index car was found at
        carChar = car[0]
        carRow = car[2]
        carCol = car[3]
        length = car[4]
        # performs a car shift 1 to the left
        # e.g. [0, "A", "A", ]
        while carCol - 1 >= 0:
          temp = board[carRow].copy()
          temp[carCol - 1] = carChar
          temp[carCol+length-1] = "0"
          tempBoard = board.copy()
          tempBoard[carRow] = temp
          children.append(tempBoard)
          carCol -= 1
        """obstacle = False

        # car shift 2 to the left
        # e.g. [0, 0, "A", "A", "A", 0]
        # or [0, 0, "A", "A", 0, 0]
        if carCol - 2 >= 0
          if str(board[carRow][carCol - 2]) != "0":
            obstacle = True
          else:
            temp = board[carRow].copy()
            temp[carCol - 2] = carChar
            temp[carCol - 1] = carChar
            if length == 2:
              temp[carCol] = 0
            temp[carCol + 1] = "0"
            temp[carCol + 2] 
            tempBoard = board.copy()
            tempBoard[carRow] = temp
            children.append(tempBoard)"""
    return children
    
for child in get_children(board):
  print(child)
  print()
  print()


        

