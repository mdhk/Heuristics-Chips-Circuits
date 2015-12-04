"""
A*
Heuristieken
"""

# Move to a lower layer without changing x and y coordinate.
# Returns id of lowest reached node
def toLowestLayer(graph, start):
    current = start
    down = current.id + graph.SURF
    while(current.adjacent.has_key(down)):
        next = graph.vertDict[down]
        next.previous = current.id
        current = next
        down = current.id + graph.SURF
    return current


import heapq
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

def weirdManhattan(target, next, current):
    initial = abs(target.x - next.x) + abs(target.y - next.y) + abs(target.z - next.z)
    bias = 0
    if current.z > next.z:
        bias = 100 
    return initial + bias

# DOES NOT WORK YET
def biasManhattan(target, next, current):
    manh = abs(target.x - next.x) + abs(target.y - next.y) + next.z
    bias = 0
    if (next.z > current.z or next.z < current.z):
       bias = -10 * (abs(target.z - next.z))
    if (current.z == next.z):
        bias = 10 * (abs(target.x - next.x) + abs(target.y - next.y))
    heur = manh + bias
    return heur



"""
aStar
Inspiratie:
    http://www.redblobgames.com/pathfinding/a-star/implementation.html
"""
# Choose heuristic function.
heuristic = normalManhattan

def aStar(graph, start, target):
    # aStar uses a heuristic to find the shortest path.
    # Start is a Vertex instance of the starting vertex.
    pq = PriorityQueue()
    pq.put(start.id, 0)
    costSoFar = {}
    costSoFar[start.id] = 0

    while not pq.empty():
        cur = pq.get()

        if cur is target.id:
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
aStarList
"""

heuristic = normalManhattan

def aStarList(graph, start, targets, target):
    pq = PriorityQueue()
    pq.put(start.id, 0)
    costSoFar = {}
    costSoFar[start.id] = 0

    while not pq.empty():
        cur = pq.get()

        if cur in targets:
            break

        for next in graph.vertDict[cur].adjacent:
            newCost = costSoFar[cur] + 1
            if next not in costSoFar or newCost < costSoFar[next]:
                costSoFar[next] = newCost
                priority = newCost + heuristic(target,
                        graph.vertDict[next], graph.vertDict[cur])
                pq.put(next, priority)
                graph.vertDict[next].previous = cur

    return cur

"""
BFS
"""
from collections import deque

def bfs(graph, start, targets):
    # NOTE: targets (formerly target) used to be a vertex instance, but is now
    # a list of id's e.g. [93] or [341, 542, 4]
    # First In First Out queue
    queue = deque([start.id])
    traversed = []
    while len(queue):
        current = queue.popleft()
        traversed.append(current)
        for v in graph.vertDict[current].adjacent:
            if v not in traversed and v not in queue:
                queue.append(v)
                if graph.vertDict[v].previous is None:
                    graph.vertDict[v].previous = current
                if (v in targets):
                    start.previous = None
                    return v

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
                next.distance = new_dist
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
