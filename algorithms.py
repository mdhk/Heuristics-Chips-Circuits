"""
A*
Inspiratie:
    http://www.redblobgames.com/pathfinding/a-star/implementation.html
"""

from Queue import PriorityQueue

def heuristicManhattan(target, next):
    # Input is in the form of a vertex object.
    # Output geeft de delta x, delta y en delta z
    return abs(target.x - next.x) + abs(target.y - next.y) + abs(target.z - next.z)

def aStar(graph, start, target):
    pq = PriorityQueue()
    pq.put( start.id, 0)
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
                priority = newCost + heuristicManhattan(target,
                        graph.vertDict[next])
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
