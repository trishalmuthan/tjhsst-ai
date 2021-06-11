import sys
from math import pi , acos , sin , cos
import heapq
import time

def get_children(parent_id):
    return graph[parent_id]

def djikstras(start_id, end_id):
    closed = set()
    fringe = [(0, start_id)]
    while fringe:
        v = heapq.heappop(fringe)
        if v[1] == end_id:
            return v
        if v[1] not in closed:
            closed.add(v[1])
            for child in get_children(v[1]):
                if child not in closed:
                    heapq.heappush(fringe, (v[0]+child[1], child[0]))
    return None

def astar(start_id, end_id):
    closed = set()
    fringe = [(calcd(locations[start_id], locations[end_id]), start_id, 0)]
    end_location = locations[end_id]
    while fringe:
        v = heapq.heappop(fringe)
        if v[1] == end_id:
            return v
        if v[1] not in closed:
            closed.add(v[1])
            for child in get_children(v[1]):
                if child not in closed:
                    heapq.heappush(fringe, (v[2]+child[1]+calcd(locations[child[0]], end_location), child[0], v[2]+child[1]))
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

structure_start = time.perf_counter()
locations = dict()
with open("rrNodes.txt") as f1:
    for line in f1:
        lineparts = line.split()
        locations[lineparts[0]] = (float(lineparts[1]), float(lineparts[2]))

cities = dict()
with open("rrNodeCity.txt") as f2:
    for line in f2:
        lineparts = line.split()
        cities[" ".join(lineparts[1:])] = lineparts[0]

graph = dict()
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
structure_end = time.perf_counter()

print(f'Time to create data structure: {structure_end-structure_start}')

dj_start = time.perf_counter()
Ddistance, Dfinal = djikstras(cities[start_city], cities[end_city])
dj_end = time.perf_counter()
print(f'{start_city} to {end_city} with Djikstra: {Ddistance} in {dj_end-dj_start}')

a_start = time.perf_counter()
Aheurisitic, Afinal, Adistance = astar(cities[start_city], cities[end_city])
a_end = time.perf_counter()
print(f'{start_city} to {end_city} with A*: {Adistance} in {a_end-a_start}')