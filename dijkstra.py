# Adapted from:
# http://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php.

import sys

class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent = {}
        self.distance = sys.maxint
        self.visited = False
        self.previous = None

    def add_neighbor(self, neighbor, weight = 1):
        self.adjacent[neighbor] = weight

    def set_distance(self, dist):
        self.distance = dist

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, id):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(id)
        self.vert_dict[id] = new_vertex
        return new_vertex

# Calculate shortest path from a given node v.
# Can be called after dijkstra finished for a given start-end pair of vertices.
def shortest(v, path):
    if v.previous:
        path.append(v.previous.id)
        shortest(v.previous, path)
        return

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
                next.set_previous(current)

        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        unvisited_queue = [(v.distance, v) for v in aGraph if not
                v.visited]
        heapq.heapify(unvisited_queue)

def apply_path(aGraph, end):
    target = aGraph.vert_dict[end]
    path = []
    path.append(target.id)
    # Traverse from target to begin of path. 
    shortest(target, path)

    print path

    # Delete connections to nodes that are in the path.
    # Currently also deletes connections to given gates (begin and end of
    # path).
    for i in range(len(path)):
        for c in aGraph.vert_dict[path[i]].adjacent.keys():
            if path[i] in aGraph.vert_dict[c].adjacent:
                print 'delete connection from: ' + str(c) + ' to: ' + \
                str(path[i])
                del(aGraph.vert_dict[c].adjacent[path[i]])

    # Clean all vertices for next search.
    for v in aGraph:
        v.distance = sys.maxint
        v.visited = False
        v.previous = None

if __name__ == '__main__':

# TEST SET
# 0  1  2  3  4
# 5  6  7  8  9
# 10 11 12 13 14
# 15 16 17 18 19

# FIND PATH FROM 17 TO 7
# THEN FIND PATH 16 TO 18

    g = Graph()
    
    HEIGHT = 4
    WIDTH = 5
    DEPTH = 1

    n = HEIGHT * WIDTH * DEPTH
    for i in range(n):
        g.add_vertex(i)

    # Create graph
    for i in range(n):
        current = g.vert_dict[i]
        if (i % WIDTH):
            current.add_neighbor(i - 1)
        if (i % WIDTH != (WIDTH -1)):
            current.add_neighbor(i + 1)
        if (i > WIDTH):
            current.add_neighbor(i - WIDTH)
        if (i < (WIDTH * HEIGHT - WIDTH)):
            current.add_neighbor(i + WIDTH)

    # FIND PATH 17 TO 7
    begin = 7
    end = 17

    # Compute first path.
    dijkstra(g, g.vert_dict[begin], g.vert_dict[end])
    # Recreate and apply the found path. 
    apply_path(g, end)

    # FIND PATH 16 TO 18
    begin = 16
    end = 18

    # Compute first path.
    dijkstra(g, g.vert_dict[begin], g.vert_dict[end])
    # Recreate and apply the found path. 
    apply_path(g, end)
