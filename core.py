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
        # self.occupied = False
        self.gate = False
        self.x = id % SURF % WIDTH 
        self.y = id % SURF / WIDTH 
        self.z = id / SURF

    def addNeighbor(self, neighbor, weight = 1):
        self.adjacent[neighbor] = weight

def connectGraph(g):
    # Connects all vertices of the graph in a grid-like manner.
    n = g.HEIGHT * g.WIDTH * g.DEPTH
    # Add vertices
    for i in range(n):
        g.addVertex(i, g.WIDTH, g.SURF)

    # Connect graph
    for v in g:
        neighbors = computeNeighbors(g, v.id)
        for n in neighbors:
            v.addNeighbor(n)

# Add connections to id from its neighbors, given that the neighbors are not
# gates and do not have paths
def connectVertex(g, id):
    neighbors = computeNeighbors(g, id)
    for i in neighbors:
        current = g.vertDict[i]
        if (not current.path) and (not current.gate):# and (not current.occupied):
            current.addNeighbor(id)

# Connects a given vertex v (with id 'id') to its neighbors, provided that
# the neighbors are not gates.
def connectNonGateVertex(g, id):
    neighbors = computeNeighbors(g, id)
    for i in neighbors:
        current = g.vertDict[i]
        if not current.gate:
            current.addNeighbor(id)

# Connects a given vertex v (with id 'id') to its neighbors, provided that
# the neighbors do not have a path.
def connectNonPathVertex(g, id):
    neighbors = computeNeighbors(g, id)
    for i in neighbors:
        current = g.vertDict[i]
        if not current.path: # and not current.occupied:
            current.addNeighbor(id)

# Delete all connections to vertices in list v.
def disconnectVertex(g, v):
    neighbors = []
    for i in v:
        neighbors = computeNeighbors(g, i)
        for n in neighbors:
            if g.vertDict[n].adjacent.has_key(i):
                del(g.vertDict[n].adjacent[i])

# Compute the neighbors of a given vertex
def computeNeighbors(g, id):
    current = g.vertDict[id]
    neighbors = []
    if current.z is not 0:
        neighbors.append(id - g.SURF)
    if current.z is not (g.DEPTH - 1):
        neighbors.append(id + g.SURF)
    if current.x is not (g.WIDTH - 1):
        neighbors.append(id + 1)
    if current.x is not 0: 
        neighbors.append(id - 1)
    if current.y is not (g.HEIGHT - 1):
        neighbors.append(id + g.WIDTH)
    if current.y is not 0:
        neighbors.append(id - g.WIDTH)
    return neighbors


# Calculate shortest path from a given node v to starting node.
def tracePath(g, v, path):
    if v.previous:
        path.append(v.previous)
        tracePath(g, g.vertDict[v.previous], path)
        return


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
    if (z == []):
        return vertices_shortest_path
    else:
        # v returnt de lengte van de kortste pad
        v = min(z)
        # slaat de pad op die het kortst is 
        index_shortest_path = z.index(v)
        verticesWithShortestPath.shortest_path = y[index_shortest_path]


    for vertex in range(len(pathsvert)):
        for path in range(len(pathsvert[vertex])):
            if (verticesWithShortestPath.shortest_path == pathsvert[vertex][path]):
                vertices_shortest_path.append(vertex)

    # print '\nPaths on every vertex: ' + str(pathsvert)
    # print '\nTotal paths on every vertex: ' + str(totalpathsvert)

    return vertices_shortest_path

# For the given netlist, return the manhattan distance between the gates. 
# ONLY WORKS IF NETLIST IS IN CORRECT FORMAT (vertex.id)
def netlistManhattan(g, netlist):
    netlistManhattan = []
    for n in netlist:
        a = g.vertDict[n[0]]
        b = g.vertDict[n[1]]
        netlistManhattan .append(abs(a.x - b.x) + abs(a.y - b.y))
    return netlistManhattan

# Return number of paths per gate.
def numberOfPaths(netlist, gateList):
    nGates = len(gateList) 
    nOfPathsList = [0 for x in range(nGates)]
    for n in netlist:
        nOfPathsList[n[0]] += 1
        nOfPathsList[n[1]] += 1
    return nOfPathsList

def numberOfPathsDict(netlist):
    nOfPathsDict = {}
    for n in netlist:
        for m in n:
            if m in nOfPathsDict:
                nOfPathsDict[m] += 1
            else:
                nOfPathsDict[m] = 1
    return nOfPathsDict

def nonGatePathNeighbors(g, gateList):
    nOfNonGateNBs = {}
    for i in gateList:
        for n in computeNeighbors(g, i):
            if n not in gateList and i not in nOfNonGateNBs and not g.vertDict[n].path:
                nOfNonGateNBs[i] = 1
            elif n not in gateList and not g.vertDict[n].path:
                nOfNonGateNBs[i] += 1
    return nOfNonGateNBs

# Remove a given path with path id 'p' from the graph, and reconnect all
# vertices in the path (to non-gates and non-path-occupied vertices).
def removePath(g, p):
    for v in g:
        if v.path == p:
            # Reconnect connections to this vertex from its non-gate neighbors. 
            connectNonGateVertex(g, v.id)
            v.path = None

# Get input from user
def user_input():
    print "In order to compute a solution for a certain circuit board, first \
enter some details about your desired configuration. Which print do you want \
to use? \nEnter 1 for print 1 (18 x 13) or 2 for print 2 (18 x 17):"
    config = 0
    netlist = 0
    while config != 1 and config != 2:
        try:
            config = int(raw_input())
        except ValueError:
            print "Please enter a number (1 or 2):"
            continue
        if config != 1 and config != 2:
            print "Please enter 1 or 2:"
            continue
        else:
            continue

    if config == 1:
        print "You have chosen print 1. Which netlist would you like to \
implement? Enter a number from 1 to 3:"
        while netlist != 1 and netlist != 2 and netlist != 3:
            try:
                netlist = int(raw_input())
            except ValueError:
                print "Please enter a number (1, 2 or 3):"
                continue
            if netlist != 1 and netlist != 2 and netlist != 3:
                print "Please enter 1, 2 or 3:"
                continue
            else:
                continue
    elif config == 2:
        print "You have chosen print 2. Which netlist would you like to \
implement? Enter a number from 4 to 6:"
        while netlist != 4 and netlist != 5 and netlist != 6:
            try:
                netlist = int(raw_input())
            except ValueError:
                print "Please enter a number (4, 5 or 6):"
                continue
            if netlist != 4 and netlist != 5 and netlist != 6:
                print "Please enter 4, 5 or 6:"
                continue
            else:
                continue

    # Loop until TOFIND paths are found.
    if netlist == 1:
        TOFIND = 30
    elif netlist == 2:
        TOFIND = 40
    elif netlist == 3 or netlist == 4:
        TOFIND = 50
    elif netlist == 5:
        TOFIND = 60
    elif netlist == 6:
        TOFIND = 70

    user_input = {"config": config, "netlist": netlist, "TOFIND": TOFIND}
    return user_input

# Convert the netlist from gates (e.g. 0 to 25) to vertex id's
def netlistConvert(WIDTH, netlist, gates):
    newnetlist = []
    for n in netlist:
        first = gates[n[0]]
        second = gates[n[1]]
        newnetlist.append([first[0] + first[1] * WIDTH, second[0] + second[1] * WIDTH])
    return newnetlist

def netlistConvert2(g, netlist, gateList):
    new_netlist = []
    for i in netlist:
        new_netlist.append((gateList[i[0]],gateList[i[1]]))
    return new_netlist

# returns for every element in the netlist, the Manhattan distance between the two gates.
def netlistCalcDist(g, new_netlist):
    netlistManhattan = []   
    for j in new_netlist:
        netlistManhattan.append(abs(g.vertDict[j[0]].x - g.vertDict[j[1]].x) + abs(g.vertDict[j[0]].y - g.vertDict[j[1]].y))
    return netlistManhattan

def short2longNetlist(new_netlist, netlistManhattan):
    dist_short_to_long_netlist = []
    for k in range(len(netlistManhattan)):
        l = netlistManhattan.index(min(netlistManhattan))
        dist_short_to_long_netlist.append(new_netlist[l])
        del netlistManhattan[l]
        del new_netlist[l]
    return dist_short_to_long_netlist

def long2shortNetlist(new_netlist, netlistManhattan):
    dist_long_to_short_netlist = []
    for k in range(len(netlistManhattan)):
        l = netlistManhattan.index(max(netlistManhattan))
        dist_long_to_short_netlist.append(new_netlist[l])
        del netlistManhattan[l]
        del new_netlist[l]
    return dist_long_to_short_netlist


def mostConnexionNetlist(g, netlist, gateList):
    a = netlistConvert2(g, netlist, gateList)
    numpaths = numberOfPaths(netlist, gateList)
    most_connexions_netlist = []

    for i in range(len(numpaths)):
        index_most_con = numpaths.index(max(numpaths))
        gate_most_con = gateList[index_most_con]
        for j in a:
            if (j[0] == gate_most_con) or (j[1] == gate_most_con):
                most_connexions_netlist.append(j)
                a.remove(j)

        del numpaths[index_most_con]
        del gateList[index_most_con]
    return most_connexions_netlist
