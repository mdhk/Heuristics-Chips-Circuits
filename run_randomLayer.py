"""
CHIPS AND CIRCUITS

run_randomLayer.py

Steps:
    while TOFIND paths are not found:
        create graph
        connect every vertex with its neighbor
        disconnect connections to gates
        compute the manhattan distance 'd' between each netlist gate pair 'n'
        for each netlist gate pair 'n' with d > 4, choose a random layer 'l' between 1 and 7
        for each n with d > 4, find the shortest part (breadth first) to layer
        a random layer 'l' and create a list of node pairs with for each index
            either n or the two nodes in layer l 
        remove the precomputed paths.
        # remove connections to the first neighbors of gates
        randomize netlist
        for each path in the netpair, compute the shortest path using
            - aStar
            - manhattan heuristic
        disconnect connections to nodes in the path
        if TOFIND paths found: break
            - return Graph
            - visualize the network

"""

from core import *
from data.config1 import width as WIDTH, height as HEIGHT, gates
from data.netlist import netlist_3 as netlist
TOFIND = 47 # Loop until TOFIND paths are found.
import algorithms
import random

DEPTH = 8
SURF = WIDTH * HEIGHT
# Show visualization (V = 1) or not (V = 0)
V = 1
S = 0
# Initialize variables that never change.
gateList = []
for c in gates:
    gateList.append(c[1] * WIDTH + c[0])

# Convert netlist to vertex id format
netlist = netlistConvert(WIDTH, netlist, gates)


"""
INITIALIZE GRAPH
"""

def run():
    # Create graph and connect it.
    g = Graph(WIDTH, HEIGHT, DEPTH, SURF)
    connectGraph(g)
    g.SURF = SURF
    g.WIDTH = WIDTH
    g.HEIGHT = HEIGHT
    g.paths = {}

    # Shuffle netlist.
    random.shuffle(netlist)

    # Remove connections to gates. 
    disconnectVertex(g, gateList)
    for i in gateList:
        g.vertDict[i].gate = True

    # Path, found, cost, time
    # Start p with 1
    p,f,c, totalTime = 1,0,0,0

    # GO TO RANDOM LAYER FIRST
    # newnetlist = []
    # for inetlist in netlist:
    #     newnetlist.append(inetlist)
    # newnetlist = netlist[:]

    newnetlist = []
    for n in netlist:
        newnetlist.append(n[:])
    # import IPython; IPython.embed()


    netlistM = netlistManhattan(g, netlist)


    for i in range(len(netlist)):
        # CHANGE PARAMETER
        if netlistM[i] > 4:
            # Go to random layer
            # CHANGE PARAMETER
            l = random.choice(range(0, 8))
            layerV = range(g.SURF * l, g.SURF * (l + 1))
            
            for j in range(2):
                found = algorithms.bfs(g, newnetlist[i][j], layerV)
                if not found:
                    continue
                path = []
                path.append(found)
                tracePath(g, g.vertDict[found], path)
                for v in g:
                    v.previous = None
                disconnectVertex(g, path)
                newnetlist[i][j] = found
                # import IPython; IPython.embed()
                for vp in path:
                    g.vertDict[vp].path = i

    # import IPython; IPython.embed()


    for n in newnetlist:
        startTime = time.time()

        start = g.vertDict[n[0]]
        target = g.vertDict[n[1]]

        # Allow connections to target gate (but only from non-gates and from
        # vertices without a pre-existing path.
        connectVertex(g, target.id)

        # Allow connections to neighbors of the target and start gates,
        # exept from nodes with a path
        for nb in computeNeighbors(g, start.id):
            if not g.vertDict[nb].gate:
                start.addNeighbor(nb)
        for nb in computeNeighbors(g, target.id):
            if not g.vertDict[nb].path and not g.vertDict[nb].gate:
                connectVertex(g, nb)

        # Compute path between start and target.
        algorithms.aStar(g, start, target)

        # Extract the previously computed path from graph g
        path = []
        path.append(target.id)

        # if len(path) == 1:
        #     # Not found: retry from original gates
        #     for v in g:
        #         if v.path == p:
        #             v.path = None
        #             v.previous = None
        #             connectVertex(g, v.id)
        #     start = g.vertDict[gateList[netlist[p][0]]]
        #     target = g.vertDict[gateList[netlist[p][1]]]
        #     algorithms.aStar(g, start, target)
        #     # import IPython; IPython.embed()

        tracePath(g, target, path)
        # Disconnect connections to the vertices in path
        disconnectVertex(g, path)

        # Assign all vertices in the path (not the gates) the path id 
        for i in path:
            cur = g.vertDict[i]
            if not cur.gate:
                # if cur.occupied:
                    # print 'CURRENT NODE ALREADY HAS PATH'
                    # import IPython; IPython.embed()
                cur.path = p
                # cur.occupied = True
        p += 1

        # Disconnect connections to the neighbors of start and target
        # NOTE: should be improved to e.g. not happen when the given gate does
        # not need any more paths. And should take into account neighboring
        # gates.
        if S:
            if start.id in gateList:
                # import IPython; IPython.embed()
                disconnectVertex(g, selectedNeighbors[gateList.index(start.id)])
            if target.id in gateList:
                disconnectVertex(g, selectedNeighbors[gateList.index(target.id)])

        # # INCORRECT
        # g.paths[p] = path

        if len(path) > 1:
            f += 1
            c += len(path) - 1

        # Prepare graph for next search.
        for v in g:
            v.previous = None
    
    # import IPython; IPython.embed()

    g.cost = c
    g.found = f
    g.newnetlist = newnetlist

    return g

if __name__ == "__main__":
    startTime = time.time()

    found = []
    m, iterations = 0, 0
    while True:
        g = run()
        iterations += 1
        if g.found > m:
            found.append(g.found)
            print 'Current max: ' + str(g.found) + 'paths '
            m = g.found
        if g.found is TOFIND:
            break

    g.totalTime = time.time() - startTime
    print '\nTotal time: ' + str(g.totalTime) + ' seconds.\n'
    print str(iterations) + ' iterations'

    n = len(netlist)
    allpaths = [[] for x in range(n)]
    for i in range(n):
        cur = []
        for v in g:
            if v.path is i:
                cur.append(v.id)
        allpaths[i] = cur
    for m in allpaths:
        print m

    import IPython; IPython.embed()

    draw.allVisualization(g, gates, TOFIND)

#     results.sort()
#     from itertools import groupby
#     resultsSorted = [len(list(group)) for key, group in groupby(results)]
#     import matplotlib.pyplot as plt
#     plt.hist(results)
#     import pylab
#     pylab.savefig('pathsfound.png')

