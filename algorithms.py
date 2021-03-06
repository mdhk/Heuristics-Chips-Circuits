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
            return cur
            # break

        for next in graph.vertDict[cur].adjacent:
            newCost = costSoFar[cur] + 1
            if next not in costSoFar or newCost < costSoFar[next]:
                costSoFar[next] = newCost
                priority = newCost + heuristic(target,
                        graph.vertDict[next], graph.vertDict[cur])
                pq.put(next, priority)
                graph.vertDict[next].previous = cur

    return 0

"""
BFS
"""
from collections import deque

def bfs(graph, start, targets):
    # NOTE: targets (formerly target) used to be a vertex instance, but is now
    # a list of id's e.g. [93] or [341, 542, 4]
    # First In First Out queue
    queue = deque([start])
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
                    return v
