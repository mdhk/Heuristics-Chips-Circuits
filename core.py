# Adapted from:
# http://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php.
"""
The 'core' describes how graphs and vertices are represented. 
Furthermore, it includes several essential functions:
 connectGraph: connect the entire graph
 disconnectVertex: disconnect a single vertex from its neighbors
 tracePath: trace back a found path from end to beginning
 applyPath: disconnect all vertices in a given array from their neighbors

disconnecting vertices (e.g. gates and paths)
"""

from config import *
import pygame, sys, time, random
import visualizations.pygameGrid as draw

class Graph:
    def __init__(self):
        self.vertDict = {}
        self.nVertices = 0

    def __iter__(self):
        return iter(self.vertDict.values())

    def addVertex(self, id):
        self.nVertices = self.nVertices + 1
        newVertex = Vertex(id)
        self.vertDict[id] = newVertex
        return newVertex

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

    def addNeighbor(self, neighbor, weight = 1):
        self.adjacent[neighbor] = weight

    def setDistance(self, dist):
        self.distance = dist

def connectGraph(g):
    # Connects all vertices of the graph in a grid-like manner.
    n = HEIGHT * WIDTH * DEPTH
    for i in range(n):
        g.addVertex(i)

    # Create graph
    for i in range(n):
        a = i % SURF
        current = g.vertDict[i]

        # In / Out connections
        if (i >= SURF):
            current.addNeighbor(i - SURF)
        if (i < (SURF * DEPTH - SURF)):
            current.addNeighbor(i + SURF)
        # Left / Right / Up / Down
        if (a % WIDTH):
            current.addNeighbor(i - 1)
        if (a % WIDTH != (WIDTH - 1)):
            current.addNeighbor(i + 1)
        if (a > WIDTH):
            current.addNeighbor(i - WIDTH)
        if (a < (SURF - WIDTH)):
            current.addNeighbor(i + WIDTH)

def disconnectVertex(g, v):
    surf = WIDTH * HEIGHT
    for i in v:
        a = i % surf
        if (i >= surf and g.vertDict[i - surf].adjacent.has_key(i)):
            del(g.vertDict[i -surf].adjacent[i])
        if (i < (surf * DEPTH - surf) and g.vertDict[i + surf].adjacent.has_key(i)):
            del(g.vertDict[i + surf].adjacent[i])
        if (a % WIDTH and g.vertDict[i - 1].adjacent.has_key(i)):
            del(g.vertDict[i - 1].adjacent[i])
        if (a % WIDTH != (WIDTH - 1) and g.vertDict[i + 1].adjacent.has_key(i)):
            del(g.vertDict[i + 1].adjacent[i])
        if (a > WIDTH and g.vertDict[i - WIDTH].adjacent.has_key(i)):
            del(g.vertDict[i - WIDTH].adjacent[i])
        if (a < (surf - WIDTH) and g.vertDict[i + WIDTH].adjacent.has_key(i)):
            del(g.vertDict[i + WIDTH].adjacent[i])

# Calculate shortest path from a given node v to starting node.
# Can be called after dijkstra finished for a given start-end pair of vertices.
def tracePath(g, v, path):
    if v.previous:
        path.append(v.previous)
        tracePath(g, g.vertDict[v.previous], path)
        return

def applyPath(g, end, begin, p):
    # Remove connections to nodes in the found path, and state what path a
    # given node participates in.
    # Compute path.
    target = g.vertDict[end]
    path = []
    path.append(target.id)

    tracePath(g, target, path)

    # Delete connections to nodes in the path.
    disconnectVertex(g, path)

    for i in path:
        g.vertDict[i].path = p

    # Prepare graph for next search.
    for v in g:
        v.distance = sys.maxint
        v.visited = False
        v.previous = None

    return path
