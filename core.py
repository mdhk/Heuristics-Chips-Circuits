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

import pygame, sys, time, random
import visualizations.pygameGrid as draw
from algorithms import aStar as algorithm

class Graph:
    def __init__(self, width, height, depth, surf):
        self.vertDict = {}
        self.WIDTH = width
        self.HEIGHT = height
        self.DEPTH = depth
        self.SURF = surf

    def __iter__(self):
        return iter(self.vertDict.values())

    def addVertex(self, id, width, surf):
        newVertex = Vertex(id, width, surf)
        self.vertDict[id] = newVertex
        return newVertex

class Vertex:
    def __init__(self, id, WIDTH, SURF):
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

def connectGraph(g):
    # Connects all vertices of the graph in a grid-like manner.
    n = g.HEIGHT * g.WIDTH * g.DEPTH
    for i in range(n):
        g.addVertex(i, g.WIDTH, g.SURF)

    # Create graph
    for i in range(n):
        a = i % g.SURF
        current = g.vertDict[i]

        # In / Out connections
        if (i >= g.SURF):
            current.addNeighbor(i - g.SURF)
        if (i < (g.SURF * g.DEPTH - g.SURF)):
            current.addNeighbor(i + g.SURF)
        # Left / Right / Up / Down
        if (a % g.WIDTH):
            current.addNeighbor(i - 1)
        if (a % g.WIDTH != (g.WIDTH - 1)):
            current.addNeighbor(i + 1)
        if (a > g.WIDTH):
            current.addNeighbor(i - g.WIDTH)
        if (a < (g.SURF - g.WIDTH)):
            current.addNeighbor(i + g.WIDTH)

def connectVertex(g, id):
    # Connects a given vertex v (with id 'id') to its neighbors, provided that
    # the neighbors are not gates and are not taken by a path.
    v = g.vertDict[id]
    for i in v.adjacent:
        current = g.vertDict[i]
        if (not current.path) and (not current.gate):
            current.addNeighbor(id)

# Delete all connections to vertices in list v.
def disconnectVertex(g, v):
    for i in v:
        a = i % g.SURF
        if (i >= g.SURF and g.vertDict[i - g.SURF].adjacent.has_key(i)):
            del(g.vertDict[i - g.SURF].adjacent[i])
        if (i < (g.SURF * g.DEPTH - g.SURF) and g.vertDict[i + g.SURF].adjacent.has_key(i)):
            del(g.vertDict[i + g.SURF].adjacent[i])
        if (a % g.WIDTH and g.vertDict[i - 1].adjacent.has_key(i)):
            del(g.vertDict[i - 1].adjacent[i])
        if (a % g.WIDTH != (g.WIDTH - 1) and g.vertDict[i + 1].adjacent.has_key(i)):
            del(g.vertDict[i + 1].adjacent[i])
        if (a > g.WIDTH and g.vertDict[i - g.WIDTH].adjacent.has_key(i)):
            del(g.vertDict[i - g.WIDTH].adjacent[i])
        if (a < (g.SURF - g.WIDTH) and g.vertDict[i + g.WIDTH].adjacent.has_key(i)):
            del(g.vertDict[i + g.WIDTH].adjacent[i])

# Calculate shortest path from a given node v to starting node.
def tracePath(g, v, path):
    if v.previous:
        path.append(v.previous)
        tracePath(g, g.vertDict[v.previous], path)
        return

def applyPath(g, start, target, p):
    # Remove connections to nodes in the found path, and state what path a
    # given node participates in.
    # Compute path.
    target = g.vertDict[target]
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


def connectallVertex(g, id):
    # Connects a given vertex v (with id 'id') to its neighbors, provided that
    # the neighbors are not gates.
    v = g.vertDict[id]
    for i in v.adjacent:
        current = g.vertDict[i]
        if (not current.gate):
            current.addNeighbor(id)

def verticesWithShortestPath(g, pathlen, pathsvert, vertices_shortest_path):
    # amount paths on every vertex
    totalpathsvert = []
    for i in range(len(pathsvert)):
        totalpathsvert.append(len(pathsvert[i]))

    # x returnt de index van de vertex waar de meeste paden over lopen
    x = totalpathsvert.index(max(totalpathsvert))
    # y is een lijst met de meeste paden die over vertex x lopen
    y = pathsvert[x]
    # z slaat de lengtes op van de paden die op de bepaalde vertex lopen
    z = []
    for i in y:
        z.append(pathlen[i])
    # v returnt de lengte van de kortste pad
    v = min(z)
    # slaat de pad op die het kortst is 
    index_shortest_path = z.index(v)
    verticesWithShortestPath.shortest_path = y[index_shortest_path]

    for vertex in range(len(pathsvert)):
        for path in range(len(pathsvert[vertex])):
            if (verticesWithShortestPath.shortest_path == pathsvert[vertex][path]):
                vertices_shortest_path.append(vertex)

    # print '\nThe most paths are going over vertex: ' + str(x)
    # print '\nPaths over ' + str(x) + ': ' + str(y)
    # print '\nLengths paths over ' + str(x) + ': ' + str(z)
    # print '\nMin length: ' + str(v) + ' from path ' + str(verticesWithShortestPath.shortest_path)
    # print '\nVertices shortest path: ' + str(vertices_shortest_path)
    # print '\nPaths on every vertex: ' + str(pathsvert)
    # print '\nTotal paths on every vertex: ' + str(totalpathsvert)

    return vertices_shortest_path