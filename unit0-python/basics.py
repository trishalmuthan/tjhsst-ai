import sys

#Problem A
if sys.argv[1] == "A":
    print(int(sys.argv[2]) + int(sys.argv[3]) + int(sys.argv[4]))
    
#Problem B
if sys.argv[1] == "B":
    count = 0
    for arg in sys.argv[2:]:
        count += int(arg)
        
    print(count)
    
#Problem C
if sys.argv[1] == "C":
    list1 = [int(arg) for arg in sys.argv[2:] if int(arg) % 3 == 0]
    print(list1)
    
#Problem D
if sys.argv[1] == "D":
    numOfFibo = int(sys.argv[2])
    first = 1
    second = 0
    for i in range(numOfFibo):
        print(first)
        store = first
        first += second
        second = store

#Problem E
if sys.argv[1] == "E":
    start = int(sys.argv[2])
    end = int(sys.argv[3])

    for num in range(start, end+1):
        answer = ((num**2) - (3*num) + 2)
        print(answer)

#Problem F
if sys.argv[1] == "F":
    side1 = float(sys.argv[2])
    side2 = float(sys.argv[3])
    side3 = float(sys.argv[4])
    if side1 + side2 < side3 or side2 + side3 < side1 or side1 + side3 < side2:
        print("The sides of your triangle are invalid!")
    else:
        s = (side1 + side2 + side3) / 2
        area = (s*(s-side1)*(s-side2)*(s-side3)) ** 0.5
        print(area)
    
#Problem G
if sys.argv[1] == "G":
    counts = { "a": 0, "e": 0, "i": 0, "o": 0, "u": 0 }
    inputStr = sys.argv[2]
    for char in inputStr:
        if char.lower() in ["a", "e", "i", "o", "u"]:
            counts[char.lower()] += 1
    print([(key, value) for key, value in counts.items()]) 