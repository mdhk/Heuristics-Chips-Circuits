# Adapted from:
# http://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php.

import pygame
import sys, time
import visualizations.array_backed_grid as draw
from data.config1 import width, height, gates

WIDTH = width
HEIGHT = height
SURF = width * height
DEPTH = 8

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

class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent = {}
        self.distance = sys.maxint
        self.visited = False
        self.previous = None
        self.path = None
        self.gate = False
        self.x = id % SURF % WIDTH 
        self.y = id % SURF / WIDTH 
        self.z = id / SURF

    def add_neighbor(self, neighbor, weight = 1):
        self.adjacent[neighbor] = weight

    def set_distance(self, dist):
        self.distance = dist

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

def connect_Graph(g):
    # Connects all vertices of the graph in a grid-like manner.
    n = HEIGHT * WIDTH * DEPTH
    for i in range(n):
        g.add_vertex(i)

    # Create graph
    for i in range(n):
        surf = WIDTH * HEIGHT
        a = i % surf
        current = g.vert_dict[i]

        # In / Out connections
        if (i >= surf):
            current.add_neighbor(i - surf)
        if (i < (surf * DEPTH - surf)):
            current.add_neighbor(i + surf)
        # Left / Right / Up / Down
        if (a % WIDTH):
            current.add_neighbor(i - 1)
        if (a % WIDTH != (WIDTH - 1)):
            current.add_neighbor(i + 1)
        if (a > WIDTH):
            current.add_neighbor(i - WIDTH)
        if (a < (surf - WIDTH)):
            current.add_neighbor(i + WIDTH)

def disconnect_vertex(aGraph, v):
    surf = WIDTH * HEIGHT
    for i in v:
        a = i % surf
        if (i >= surf and aGraph.vert_dict[i - surf].adjacent.has_key(i)):
            del(aGraph.vert_dict[i -surf].adjacent[i])
        if (i < (surf * DEPTH - surf) and aGraph.vert_dict[i + surf].adjacent.has_key(i)):
            del(aGraph.vert_dict[i + surf].adjacent[i])
        if (a % WIDTH and aGraph.vert_dict[i - 1].adjacent.has_key(i)):
            del(aGraph.vert_dict[i - 1].adjacent[i])
        if (a % WIDTH != (WIDTH - 1) and aGraph.vert_dict[i + 1].adjacent.has_key(i)):
            del(aGraph.vert_dict[i + 1].adjacent[i])
        if (a > WIDTH and aGraph.vert_dict[i - WIDTH].adjacent.has_key(i)):
            del(aGraph.vert_dict[i - WIDTH].adjacent[i])
        if (a < (surf - WIDTH) and aGraph.vert_dict[i + WIDTH].adjacent.has_key(i)):
            del(aGraph.vert_dict[i + WIDTH].adjacent[i])

# Calculate shortest path from a given node v to starting node.
# Can be called after dijkstra finished for a given start-end pair of vertices.
def shortest(aGraph, v, path):
    if v.previous:
        path.append(v.previous)
        shortest(aGraph, aGraph.vert_dict[v.previous], path)
        return

def apply_path(aGraph, end, begin, p):
    # Remove connections to nodes in the found path, and state what path a
    # given node participates in.
    # Compute path.
    target = aGraph.vert_dict[end]
    path = []
    path.append(target.id)

    shortest(aGraph, target, path)
    print path

    # Delete connections to nodes in the path.
    disconnect_vertex(aGraph, path)

    for i in path:
        aGraph.vert_dict[i].path = p

    # Prepare graph for next search.
    for v in aGraph:
        v.distance = sys.maxint
        v.visited = False
        v.previous = None

    return path
