import tkinter as tk
import sys
from math import pi , acos , sin , cos
import heapq
import time

def get_children(parent_id):
    return graph[parent_id]

def djikstras(start_id, end_id):
    closed = set()
    fringe = [(0, start_id, None, None)]
    updateCount = 0
    while fringe:
        v = heapq.heappop(fringe)
        if v[1] == end_id:
            store = v
            while store is not None:
                canvas1.itemconfig(store[3], fill="#28C638")
                store = store[2]
            root1.update()
            time.sleep(5)
            root1.destroy()
            return v
        if v[1] not in closed:
            closed.add(v[1])
            for child in get_children(v[1]):
                if child not in closed:
                    if (v[1], child[0]) in edges:
                        line = edges[(v[1], child[0])]
                        heapq.heappush(fringe, (v[0]+child[1], child[0], v, line))
                        canvas1.itemconfig(line, fill="red")
                        updateCount += 1
                        if updateCount == 2000:
                            root1.update()
                            updateCount = 0
                    else:
                        line = edges[(child[0], v[1])]
                        heapq.heappush(fringe, (v[0]+child[1], child[0], v, line))
                        canvas1.itemconfig(line, fill="red")
                        updateCount += 1
                        if updateCount == 2000:
                            root1.update()
                            updateCount = 0
    return None

def astar(start_id, end_id):
    closed = set()
    fringe = [(calcd(locations[start_id], locations[end_id]), start_id, 0, None, None)]
    end_location = locations[end_id]
    updateCount = 0
    while fringe:
        v = heapq.heappop(fringe)
        if v[1] == end_id:
            store = v
            while store is not None:
                canvas2.itemconfig(store[4], fill="#28C638")
                store = store[3]            
            root2.update()
            time.sleep(5)
            root2.destroy()
            return v
        if v[1] not in closed:
            closed.add(v[1])
            for child in get_children(v[1]):
                if child not in closed:
                    if (v[1], child[0]) in edges:
                        line = edges[(v[1], child[0])]
                        heapq.heappush(fringe, (v[2]+child[1]+calcd(locations[child[0]], end_location), child[0], v[2]+child[1], v, line))
                        canvas2.itemconfig(line, fill="#F7AD1A")
                        updateCount += 1
                        if updateCount == 300:
                            root2.update()
                            updateCount = 0
                    else:
                        line = edges[(child[0], v[1])]
                        heapq.heappush(fringe, (v[2]+child[1]+calcd(locations[child[0]], end_location), child[0], v[2]+child[1], v, line))
                        canvas2.itemconfig(line, fill="#F7AD1A")
                        updateCount += 1
                        if updateCount == 300:
                            root2.update()
                            updateCount = 0
    return None

def calcd(node1, node2):
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees
   if node1 == node2:
       return 0

   y1, x1 = node1
   y2, x2 = node2

   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

start_city= sys.argv[1]
end_city = sys.argv[2]

CANVAS_SIZE = 800
root1 = tk.Tk()
root1.title(f'Djikstras Algorithm: {start_city} to {end_city}')
canvas1 = tk.Canvas(root1, height=CANVAS_SIZE, width=CANVAS_SIZE, bg='#4E644E')

locations = dict()
with open("rrNodes.txt") as f1:
    for line in f1:
        lineparts = line.split()
        locations[lineparts[0]] = (float(lineparts[1]), float(lineparts[2]))

latMax = max([lat for lat, lon in locations.values()])
longitudes = [lon for lat, lon in locations.values()]
lonMin = min(longitudes)
lonMax = max(longitudes)

structure_start = time.perf_counter()
cities = dict()
with open("rrNodeCity.txt") as f2:
    for line in f2:
        lineparts = line.split()
        cities[" ".join(lineparts[1:])] = lineparts[0]

graph = dict()
edges = dict()
with open("rrEdges.txt") as f:
    for line in f:
        lineparts = line.split()
        distance = calcd(locations[lineparts[0]], locations[lineparts[1]])
        if lineparts[0] in graph:
            graph[lineparts[0]].append((lineparts[1], distance))
        else:
            graph[lineparts[0]] = [(lineparts[1], distance)]
        if lineparts[1] in graph:
            graph[lineparts[1]].append((lineparts[0], distance))
        else:
            graph[lineparts[1]] = [(lineparts[0], distance)]
        edges[(lineparts[0], lineparts[1])] = canvas1.create_line(((locations[lineparts[0]][1]+(-lonMin))/(lonMax-lonMin))*CANVAS_SIZE, CANVAS_SIZE-((abs(locations[lineparts[0]][0])/latMax)*CANVAS_SIZE), ((locations[lineparts[1]][1]+(-lonMin))/(lonMax-lonMin))*CANVAS_SIZE, CANVAS_SIZE-((abs(locations[lineparts[1]][0])/latMax)*CANVAS_SIZE), fill="white", width=1.2)
structure_end = time.perf_counter()
canvas1.pack(expand=True)


print(f'Time to create data structure: {structure_end-structure_start}')

dj_start = time.perf_counter()
Ddistance, Dfinal, Dparent, Dline = djikstras(cities[start_city], cities[end_city])
dj_end = time.perf_counter()
print(f'{start_city} to {end_city} with Djikstra: {Ddistance} in {dj_end-dj_start}')
root1.mainloop()

root2 = tk.Tk()
root2.title(f'A* Algorithm: {start_city} to {end_city}')
canvas2 = tk.Canvas(root2, height=CANVAS_SIZE, width=CANVAS_SIZE, bg='#4E644E')

graph = dict()
edges = dict()
with open("rrEdges.txt") as f:
    for line in f:
        lineparts = line.split()
        distance = calcd(locations[lineparts[0]], locations[lineparts[1]])
        if lineparts[0] in graph:
            graph[lineparts[0]].append((lineparts[1], distance))
        else:
            graph[lineparts[0]] = [(lineparts[1], distance)]
        if lineparts[1] in graph:
            graph[lineparts[1]].append((lineparts[0], distance))
        else:
            graph[lineparts[1]] = [(lineparts[0], distance)]
        edges[(lineparts[0], lineparts[1])] = canvas2.create_line(((locations[lineparts[0]][1]+(-lonMin))/(lonMax-lonMin))*CANVAS_SIZE, CANVAS_SIZE-((abs(locations[lineparts[0]][0])/latMax)*CANVAS_SIZE), ((locations[lineparts[1]][1]+(-lonMin))/(lonMax-lonMin))*CANVAS_SIZE, CANVAS_SIZE-((abs(locations[lineparts[1]][0])/latMax)*CANVAS_SIZE), fill="white", width=1.2)
structure_end = time.perf_counter()
canvas2.pack(expand=True)

a_start = time.perf_counter()
Aheurisitic, Afinal, Adistance, Aparent, Aline = astar(cities[start_city], cities[end_city])
a_end = time.perf_counter()
print(f'{start_city} to {end_city} with A*: {Adistance} in {a_end-a_start}')
root2.mainloop()

