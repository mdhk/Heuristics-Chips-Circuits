"""
A*
Inspiratie:
    http://www.redblobgames.com/pathfinding/a-star/implementation.html
"""

import heapq

# from Queue import PriorityQueue

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def normalManhattan(target, next, current):
    # Input is in the form of a vertex object.
    # Output is delta x, delta y and delta z
    return abs(target.x - next.x) + abs(target.y - next.y) + abs(target.z - next.z)

# DOES NOT WORK YET
def biasManhattan(target, next, current):
    manh = abs(target.x - next.x) + abs(target.y - next.y) + abs(target.z - next.z)
    bias = 0
    if (next.z > current.z or next.z < current.z):
       bias = -10 * (abs(target.z - next.z))
    if (current.z == next.z):
        bias = 10 * (abs(target.x - next.x) + abs(target.y - next.y))
    heur = manh + bias
    return heur

heuristic = normalManhattan

"""
weird_aStar
"""

def weird_aStar(graph, start, target, p):
    from core import *
    from config import *
    temp = start
    current = temp
    while (current.adjacent.has_key(current.id + SURF)):
        next = graph.vertDict[current.id + SURF]
        next.previous = current.id
        current = next
        temp.id = current.id

    applyPath(graph, current.id, start.id, p)
    print current.id
    start = current

    pq = PriorityQueue()
    pq.put(start.id, 0)
    costSoFar = {}
    costSoFar[start.id] = 0

    while not pq.empty():
        cur = pq.get()

        if cur == target.id:
            break

        for next in graph.vertDict[cur].adjacent:
            newCost = costSoFar[cur] + 1
            if next not in costSoFar or newCost < costSoFar[next]:
                costSoFar[next] = newCost
                priority = newCost + heuristic(target,
                        graph.vertDict[next], graph.vertDict[cur])
                pq.put(next, priority)
                graph.vertDict[next].previous = cur

"""
aStar
"""
def aStar(graph, start, target):
    pq = PriorityQueue()
    pq.put(start.id, 0)
    costSoFar = {}
    costSoFar[start.id] = 0

    while not pq.empty():
        cur = pq.get()

        if cur == target.id:
            break

        for next in graph.vertDict[cur].adjacent:
            newCost = costSoFar[cur] + 1
            if next not in costSoFar or newCost < costSoFar[next]:
                costSoFar[next] = newCost
                priority = newCost + heuristic(target,
                        graph.vertDict[next], graph.vertDict[cur])
                pq.put(next, priority)
                graph.vertDict[next].previous = cur

"""
BFS
"""
from collections import deque

def bfs(graph, start, target):
    # First In First Out queue
    queue = deque([start.id])
    traversed = []
    found = False
    while (not found and len(queue)):
        current = queue.popleft()
        traversed.append(current)
        for v in graph.vertDict[current].adjacent:
            if v not in traversed and v not in queue:
                queue.append(v)
                if graph.vertDict[v].previous is None:
                    graph.vertDict[v].previous = current
                if (v == target.id):
                    start.previous = None
                    found = True

"""
DIJKSTRA
"""

import heapq

def dijkstra(graph, start, target):
    start.setDistance(0)

    unvisitedQueue = [(v.distance, v) for v in graph]
    heapq.heapify(unvisitedQueue)

    while len(unvisitedQueue):
        uv = heapq.heappop(unvisitedQueue)
        current = uv[1]
        current.visited = True

        for next in current.adjacent:
            next = graph.vertDict[next]
            if next.visited:
                continue
            new_dist = current.distance + 1

            if new_dist < next.distance:
                next.setDistance(new_dist)
                next.previous = current.id
        
        # Note: probably not optimal to clear queue and build it up again every
        # time.. 
        while len(unvisitedQueue):
            heapq.heappop(unvisitedQueue)
        unvisitedQueue = [(v.distance, v) for v in graph if not
                v.visited]
        heapq.heapify(unvisitedQueue)

        # When target has been visited, break
        if target.visited:
            break
