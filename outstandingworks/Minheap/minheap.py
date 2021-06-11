import sys

class MinHeap():
    def __init__(self):
        #This is to index at 1
        self.Heap = [0]
        #Keep track of size
        self.Size = 0
    
    def __str__(self):
        #Print out the heap as a list
        return str(self.Heap[1:])

    def heappush(self, item):
        #Add item to end of list and increase size by 1
        self.Heap.append(item)
        self.Size += 1
        #heapUp method to retain heap property and move newly added element to correct position
        self.heapUp()

    def heapUp(self):
        #i is equal to initial index of element at the end of list
        i = self.Size
        #while i has a parent
        while i // 2 > 0:
            #if current node is less than parent
            if self.Heap[i] < self.Heap[i // 2]:
                #swap current and parent
                temp = self.Heap[i // 2]
                self.Heap[i // 2] = self.Heap[i]
                self.Heap[i] = temp
            #end while loop because correct location is found
            else:
                break
            #set i equal to new location
            i = i // 2
        #newly added node will now be in satisfying posiiton

    def heapify(self, l1):
        #For every element in the list, add it to the end of the heap, increase size by 1, and call the heapUp method
        for item in l1:
            self.Heap.append(item)
            self.Size += 1
            self.heapUp()

    def heappop(self):
        #Store removed value, set new root to the item at the end of the list, decrease size by 1, eliminate last element from list, call heapDown
        # to retain heap property and move swapped element to correct position, and return removed value
        value = self.Heap[1]
        self.Heap[1] = self.Heap[self.Size]
        self.Size -= 1
        self.Heap.pop()
        self.heapDown()
        return value

    def heapDown(self):
        #Set i to index of root
        i = 1
        #While current node has a left child
        while 2*i <= self.Size:
            #store index of min child of left and right
            swapChild = self.pickMinChild(i)
            #if current node is greater than the minimum child, swap nodes
            if self.Heap[i] > self.Heap[swapChild]:
                temp = self.Heap[i]
                self.Heap[i] = self.Heap[swapChild]
                self.Heap[swapChild] = temp
            #end while loop because correct location is found
            else:
                break
            #set i equal to new location
            i = swapChild

    def pickMinChild(self, i):
        #If no right child return left child
        if 2 * i + 1 > self.Size:
            return i * 2
        #Return bigger of left and right child
        else:
            if self.Heap[2*i] < self.Heap[2*i+1]:
                return 2 * i
            else:
                return 2 * i + 1

    def getmin(self):
        #Return the first element in the Heap List
        return self.Heap[1]

#Create MinHeap 
heap = MinHeap()

#Create a list, loop through arguments and add to list. Keep track of index of first A or R when found and break.
list1 = list()
index = 0
for count, arg in enumerate(sys.argv[1:], 1):
    if arg == "A" or arg == "R":
        index = count
        break
    else:
        list1.append(int(arg))

#Print list
print("Initial list: " + str(list1))
#Heapify and print heap
heap.heapify(list1)
print("Heapified list: " + str(heap))

#Loop through arguments starting from first letter
for arg in sys.argv[index:]:
    #If argument is an R, remove element from heap and print
    if arg == "R":
        print(f"Popped {heap.heappop()} from heap: " + str(heap))
    #Else, if it is not A (meaning it's a number), add that number to the heap and print
    elif arg != "A":
        heap.heappush(int(arg))
        print(f"Added {int(arg)} to heap: " + str(heap))


