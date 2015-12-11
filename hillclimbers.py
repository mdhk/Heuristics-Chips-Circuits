# standardHillClimber removes removeNPaths paths and subsequently tries to lay
# all remaining paths using a shortest path algorithm.
import random
import algorithms
from core import *
def standardHillClimber(gcopy, maxNPaths, removeNPaths):
    # Compute what paths have been found already. 
    # Assumes that v.path starts counting at 1.
    foundPaths = []
    toFindPaths = []
    for i in range(maxNPaths):
        if gcopy.connectedPaths[i]:
            foundPaths.append(i)
        else:
            toFindPaths.append(i)

    toRemove = random.sample(foundPaths, removeNPaths)
    

    # Remove the sampled paths
    for i in toRemove:
        toFindPaths.append(i)

    # Remove unfinished paths (where only a path to a random layer exists).
    for i in toFindPaths:
        removePath(gcopy, i)
        gcopy.connectedPaths[i] = False

    # Reconnect all vertices with their neighbors that are not gates or have
    # paths
    for v in gcopy:
        if not v.path and not v.gate:
            nb = computeNeighbors(gcopy, v.id)
            for i in nb:
                cur = gcopy.vertDict[i]
                if not cur.path and not cur.gate:
                    cur.addNeighbor(v.id)

    # Randomize the order in which new netlist paths are computed.
    random.shuffle(toFindPaths)

    # import IPython; IPython.embed();

    gcopy.found -= removeNPaths
    # toFindPaths can be from 0 to e.g. 49
    for i in toFindPaths:
        n = gcopy.netlist[i]
        start = n[0]
        target = n[1]
        algorithms.aStar(gcopy, gcopy.vertDict[start], gcopy.vertDict[target])
        path = []
        path.append(target)
        tracePath(gcopy, gcopy.vertDict[target], path)
        disconnectVertex(gcopy, path)
        for j in path:
            cur = gcopy.vertDict[j]
            if not cur.gate:
                cur.path = i + 1
        if len(path) > 1:
            gcopy.found += 1
            gcopy.cost += len(path) - 1
            gcopy.connectedPaths[i] = True
        for v in gcopy:
    
            v.previous = None
