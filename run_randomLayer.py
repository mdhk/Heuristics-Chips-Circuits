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
TOFIND = 50 # Loop until TOFIND paths are found.
MAXITERATIONS = 500
import algorithms, random, copy, hillclimbers

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

def run():
    startTime = time.time()

    # Create graph and connect it.
    g = Graph(WIDTH, HEIGHT, DEPTH, SURF)
    connectGraph(g)
    g.SURF = SURF
    g.WIDTH = WIDTH
    g.HEIGHT = HEIGHT
    g.connectedPaths = [False for x in range(len(netlist))]

    # Shuffle netlist.
    random.shuffle(netlist)
    # Compute manhattan distance between netlist gate pairs. 
    netlistM = netlistManhattan(g, netlist)

    # Remove connections to gates. 
    disconnectVertex(g, gateList)
    for i in gateList:
        g.vertDict[i].gate = True

    # Path, found, cost, time
    # Start p with 1
    p,f,c, totalTime = 1,0,0,0

    # Copy netlist (without maintaining references)
    newnetlist = copy.deepcopy(netlist)

    # If possible, generate a shortest path from both gate pairs in the netlist
    # iteration to a random layer. 
    for i in range(len(netlist)):
        # Depending on manhattan distance between netlist gate pairs. 
        if netlistM[i] > 4:
            # Choose random layer.
            l = random.choice(range(1, 8))
            # Create list of all nodes in layer l.
            layerV = range(g.SURF * l, g.SURF * (l + 1))

            foundFirst = algorithms.bfs(g, newnetlist[i][0], layerV)
            if not foundFirst:
                for v in g:
                    v.previous = None
                continue
            pathFirst = []
            pathFirst.append(foundFirst)
            tracePath(g, g.vertDict[foundFirst], pathFirst)
            for v in g:
                v.previous = None

            foundSecond = algorithms.bfs(g, newnetlist[i][1], layerV)
            if not foundSecond:
                for v in g:
                    v.previous = None
                continue
            pathSecond = []
            pathSecond.append(foundSecond)
            tracePath(g, g.vertDict[foundSecond], pathSecond)

            for v in g:
                v.previous = None
            disconnectVertex(g, pathFirst)
            disconnectVertex(g, pathSecond)

            newnetlist[i][0] = foundFirst
            newnetlist[i][1] = foundSecond

            for vp in pathFirst:
                g.vertDict[vp].path = i + 1
            for vp in pathSecond:
                g.vertDict[vp].path = i + 1

    # Find paths between the (updated) netlist vertex pairs.
    for n in newnetlist:
    # for n in newnetlist[1:30]:
        start = g.vertDict[n[0]]
        target = g.vertDict[n[1]]

        # Allow connections to target gate (but only from non-gates and from
        # vertices without a pre-existing path.
        connectVertex(g, target.id)

        # Add connections from start to non-gate non-path neighbors.
        for nb in computeNeighbors(g, start.id):
            if not g.vertDict[nb].path and not g.vertDict[nb].gate:
                start.addNeighbor(nb)
        # Add connections from non-gate non-path neighbors to target vertex. 
        for nb in computeNeighbors(g, target.id):
            if not g.vertDict[nb].path and not g.vertDict[nb].gate:
                g.vertDict[nb].addNeighbor(target.id)

        # Compute path between start and target.
        algorithms.aStar(g, start, target)

        # Extract the computed path and disconnect these vertices. 
        path = []
        path.append(target.id)
        tracePath(g, target, path)
        disconnectVertex(g, path)

        if len(path) > 1:
            f += 1
            c += len(path) - 1
            g.connectedPaths[p - 1] = True
        # else:
        #     print 'not found'

        # Assign all vertices in the path (not the gates) the path id 
        for i in path:
            cur = g.vertDict[i]
            if not cur.gate:
                cur.path = p
        p += 1

        # Prepare graph for next search.
        for v in g:
            v.previous = None

    g.cost = c
    g.found = f
    g.newnetlist = newnetlist
    g.netlist = netlist

    return g

if __name__ == "__main__":
    startTime = time.time()

    found = []
    m, iterations = 0, 0
    print 'To find: ' + str(TOFIND)
    print 'Iterations until hillclimbing: ' + str(MAXITERATIONS)
    while True:
        g = run()
        iterations += 1
        print iterations
        found.append(g.found)
        if g.found > m:
            print 'Current max: ' + str(g.found) + 'paths '
            gMax = copy.deepcopy(g)
            m = g.found
        # if g.found is TOFIND:
        #     break
        if (iterations >= MAXITERATIONS) or (g.found is TOFIND):
            break

    # import IPython; IPython.embed()
    n = len(netlist)

    # Hillclimber session
    iterations = 0
    found = g.found
    g = gMax
    print 'Starting hillclimber'
    print 'Paths found at start hillclimber session: ' + str(gMax.found)
    print 'Number of paths in netlist: ' + str(n)
    while not (found == n) and (iterations <= MAXITERATIONS):
        gcopy = copy.deepcopy(g)
        nRemovePaths = random.randint(2,15)
        hillclimbers.standardHillClimber(gcopy, n, nRemovePaths)
        iterations += 1
        if gcopy.found > g.found:
            g = copy.deepcopy(gcopy)
            found = g.found
            print 'new: ' + str(found)
        print 'No improvement: ' + str(gcopy.found)

    g.totalTime = time.time() - startTime
    print '\nTotal time: ' + str(g.totalTime) + ' seconds.\n'
    print str(iterations) + ' iterations'

    allpaths = [[] for x in range(n)]
    for i in range(n):
        cur = []
        for v in g:
            if v.path is i + 1:
                cur.append(v.id)
        allpaths[i] = cur
    for m in allpaths:
        print m

    import IPython; IPython.embed()

    # found.sort()
    # from itertools import groupby
    # foundSorted = [len(list(group)) for key, group in groupby(found)]
    # import matplotlib.pyplot as plt
    # plt.hist(found)
    # import pylab
    # pylab.savefig('run_randomLayer_results_netlist6_61.png')

    import toThreejs
    toThreejs.convert(g)

    draw.allVisualization(g, gates, TOFIND)
