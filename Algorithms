"""
A*
Inspiratie:
    http://www.redblobgames.com/pathfinding/a-star/implementation.html
"""

from Queue import PriorityQueue

def heuristicManhattan(goal, next):
    # Input is in the form of a vertex object.
    # Output geeft de delta x, delta y en delta z
    return abs(goal.x - next.x) + abs(goal.y - next.y) + abs(goal.z - next.z)

def aStar(aGraph, start, target):
    pq = PriorityQueue()
    pq.put( start.id, 0)
    costSoFar = {}
    costSoFar[start.id] = 0

    while not pq.empty():
        cur = pq.get()

        if cur == target.id:
            break

        for next in aGraph.vert_dict[cur].adjacent:
            newCost = costSoFar[cur] + 1
            if next not in costSoFar or newCost < costSoFar[next]:
                costSoFar[next] = newCost
                priority = newCost + heuristicManhattan(target,
                        aGraph.vert_dict[next])
                pq.put(next, priority)
                aGraph.vert_dict[next].previous = cur

    if not target.previous:
        print '############################################## Not found! ############################################'

"""
BFS
"""
from collections import deque

def bfs(aGraph, start, target):
    # First In First Out queue
    queue = deque([start.id])
    traversed = []
    found = False
    while (not found and len(queue)):
        current = queue.popleft()
        traversed.append(current)
        for v in aGraph.vert_dict[current].adjacent:
            if v not in traversed and v not in queue:
                queue.append(v)
                if aGraph.vert_dict[v].previous is None:
                    aGraph.vert_dict[v].previous = current
                if (v == target.id):
                    start.previous = None
                    found = True
    
    if not found:
        print '############################################## Not found! ############################################'

"""
DIJKSTRA
"""

import heapq

def dijkstra(aGraph, start, target):
    start.set_distance(0)

    unvisited_queue = [(v.distance, v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        for next in current.adjacent:
            next = aGraph.vert_dict[next]
            if next.visited:
                continue
            new_dist = current.distance + 1

            if new_dist < next.distance:
                next.set_distance(new_dist)
                next.set_previous(current.id)
        
        # Note: probably not optimal to clear queue and build it up again every
        # time.. 
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        unvisited_queue = [(v.distance, v) for v in aGraph if not
                v.visited]
        heapq.heapify(unvisited_queue)

        # When target has been visited, break
        if target.visited:
            break