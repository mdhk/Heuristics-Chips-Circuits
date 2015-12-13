"""
CHIPS AND CIRCUITS

run_randomLayer.py

Steps:
    while TOFIND paths are not found:
        randomize netlist



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

def run():
    # startTime = time.time()

    """
    INITIALIZE GRAPH AND VARIABLES
    """

    # Create graph and connect it. Keep track of what paths have been
    # connected.
    g = Graph(WIDTH, HEIGHT, DEPTH, SURF)
    connectGraph(g)
    g.connectedPaths = [False for x in range(N)]
    # Remove connections to gates.
    disconnectVertex(g, gateList)
    for i in gateList:
        g.vertDict[i].gate = True

    # Randomize the order in which netlist paths are computed.
    random.shuffle(netlist)

    # Initialize path, found, cost, time
    p,g.found,g.cost, totalTime = 1,0,0,0
    newnetlist = copy.deepcopy(netlist)
    netlistMH = netlistManhattan(g, newnetlist)

    # If gates have the same number of non-gate/non-path neighbors as paths
    # they should make, reserve these neighbors for the given gate(s).
    for iter in range(5):
        nPaths = numberOfPathsDict(newnetlist)
        nNonGateNeighbors = nonGatePathNeighbors(g, gateList)
        for n in gateList:
            if n not in nPaths:
                continue
            if nPaths[n] == nNonGateNeighbors[n]:
                # What paths does this gate belong to?
                pathNumber = []
                index = []
                for i in range(N):
                    if newnetlist[i][0] == n:
                        pathNumber.append(i + 1)
                        index.append(0)
                    elif newnetlist[i][1] == n:
                        index.append(1)
                        pathNumber.append(i + 1)
                # Reserve each neighbor for a specific path and disconnect it.
                ind = range(len(pathNumber))
                random.shuffle(ind)
                nb = list(g.vertDict[n].adjacent)
                # import IPython; IPython.embed()
                for i in ind:
                    g.vertDict[nb[i]].path = pathNumber[i]
                    newnetlist[pathNumber[i]-1][index[i]] = nb[i]
                disconnectVertex(g, nb)

    # import IPython; IPython.embed()

    # If possible, generate a shortest path from both gate pairs in the netlist
    # iteration to (the same) random layer. 
    for i in range(N):
        # Depending on manhattan distance between netlist gate pairs. 
        if netlistMH[i] > MIN_MANHATTAN:
            # import IPython; IPython.embed()

            # Choose random layer.
            l = random.choice(range(0, 8))
            # List nodes in layer 'l'.
            lVertices = range(g.SURF * l, g.SURF * (l + 1))

            # import IPython; IPython.embed()
            cur = g.vertDict[newnetlist[i][0]]
            foundFirst = algorithms.aStarList(g, cur, lVertices, g.vertDict[cur.id - g.SURF * cur.z + g.SURF * l])
            if not foundFirst:
                for v in g:
                    v.previous = None
                # If no path from layer 0 to layer l was found, continue with
                # next iteration.
                # print 'not found FIRST'
                continue
            else:
                pathFirst = []
                pathFirst.append(foundFirst)
                tracePath(g, g.vertDict[foundFirst], pathFirst)
                for v in g:
                    v.previous = None

            cur = g.vertDict[newnetlist[i][1]]
            # foundSecond = algorithms.aStarList(g, cur, lVertices, cur - g.SURF * cur.z + g.SURF * l)
            # foundSecond = algorithms.aStarList(g, g.vertDict[newnetlist[i][1]], lVertices, g.vertDict[newnetlist[i][1] + g.SURF * l])
            foundSecond = algorithms.aStarList(g, cur, lVertices, g.vertDict[cur.id - g.SURF * cur.z + g.SURF * l])
            if not foundSecond:
                # print 'not found SECOND'
                for v in g:
                    v.previous = None
                continue

            pathSecond = []
            pathSecond.append(foundSecond)
            tracePath(g, g.vertDict[foundSecond], pathSecond)
            for v in g:
                v.previous = None

            for vp in pathFirst:
                g.vertDict[vp].path = i + 1
            for vp in pathSecond:
                g.vertDict[vp].path = i + 1

            disconnectVertex(g, pathFirst)
            disconnectVertex(g, pathSecond)

            newnetlist[i][0] = foundFirst
            newnetlist[i][1] = foundSecond

    # newnetlist has been updated, now disconnect the remaining neighbors of
    # all start/target nodes.
    if D:
        for i in newnetlist:
            disconnectVertex(g, computeNeighbors(g, i[0]))
            disconnectVertex(g, computeNeighbors(g, i[1]))

    g.newnetlist = copy.deepcopy(newnetlist)

    # Try to find the complete path list twice (some neighbors of
    # starting/target nodes might be disconnected on the first iteration but
    # connected on the second iteration.
    for x in range(2):
        p = 0

        for i in range(N):
            if g.connectedPaths[i]:
                newnetlist[i] = [0, 0]

        # Find paths between the (updated) netlist vertex pairs.
        for n in newnetlist:
            p += 1
            if n == [0, 0]:
                continue
            start = g.vertDict[n[0]]
            target = g.vertDict[n[1]]

            # Reconnect neighbors of start and target node.
            if D:
                nb = computeNeighbors(g, start.id) + computeNeighbors(g, target.id)
                for i in nb:
                    if not (g.vertDict[i].path) and not (g.vertDict[i].gate):
                        connectVertex(g, i)

            # Reconnect connections to target 
            connectVertex(g, target.id)
            # Reconnect connections from start to its neighbors
            for nb in computeNeighbors(g, start.id):
                if not g.vertDict[nb].path and not g.vertDict[nb].gate:
                    start.addNeighbor(nb)

            # Compute path between start and target.
            algorithms.aStar(g, start, target)

            # Extract the computed path and disconnect these vertices. 
            path = []
            path.append(target.id)
            tracePath(g, target, path)
            disconnectVertex(g, path)

            if len(path) > 1:
                g.found += 1
                g.cost += len(path) - 1
                g.connectedPaths[p - 1] = True

            # Assign all vertices in the path (not the gates) the path id 
            for i in path:
                cur = g.vertDict[i]
                if not cur.gate:
                    cur.path = p

            # Prepare graph for next search.
            for v in g:
                v.previous = None

    g.netlist = netlist

    return g

if __name__ == "__main__":
    # startTime = time.time()

    # # Keep track of what gates are difficult to connect:
    # notConnected = {}
    # for i in gateList:
    #     notConnected[i] = 0

    """
    USER INPUT
    """

    from core import *
    from data.netlist import *
    import algorithms, random, copy, hillclimbers

    # get user input
    user_input = user_input()

    # set config from user input
    if user_input["config"] == 1:
        from data.config1 import width as WIDTH, height as HEIGHT, gates
    elif user_input["config"] == 2:
        from data.config2 import width as WIDTH, height as HEIGHT, gates

    # set netlist and number of paths to find from user input
    netlist = netlists[user_input["netlist"] - 1]
    TOFIND = user_input["TOFIND"]
    N = len(netlist)

    # from data.config1 import width as WIDTH, height as HEIGHT, gates
    # from data.netlist import netlist_3 as netlist
    # TOFIND = 50 # Loop until TOFIND paths are found.
    MAX_LAYER_ITERATIONS = 10000
    MAX_HILLCLIMBER = 500
    MIN_MANHATTAN = 3

    DEPTH = 8
    SURF = WIDTH * HEIGHT
    # Show visualization (V = 1) or not (V = 0)
    V = 1
    # Disconnect neighbors
    D = 1
    # Optimize after initial run() (Hillclimber)
    O = 1
    # Initialize variables that never change.
    gateList = []
    for c in gates:
        gateList.append(c[1] * WIDTH + c[0])

    # Convert netlist to vertex id format
    netlist = netlistConvert(WIDTH, netlist, gates)

    import pickle

    found = []
    m, iterations = 0, 0
    print 'To find: ' + str(TOFIND)
    print 'Iterations until hillclimbing: ' + str(MAX_LAYER_ITERATIONS)
    while True:
        g = run()
        iterations += 1
        if not iterations % 1000:
            print iterations
        # print iterations
        found.append(g.found)
        if g.found > m:
            # with open('randomLayerNL6_Nfound6.pkl', 'wb') as output:
            #     pickle.dump(g, output, pickle.HIGHEST_PROTOCOL)

            # notConnected = {}
            # for i in gateList:
            #     notConnected[i] = 0

            glist = []
            # print 'Current max: ' + str(g.found) + 'paths '
            # gMax = copy.deepcopy(g)
            m = g.found
        # if g.found is TOFIND:
        #     break
        if (g.found == m):
            glist.append(copy.deepcopy(g))
            print 'Newly found: ' + str(m) + ', ' + str(len(glist)) + ' times.'

            # for i in range(len(g.connectedPaths)):
            #     if not g.connectedPaths[i]:
            #         for nc in g.netlist[i]:
            #             notConnected[nc] += 1

        if (iterations >= MAX_LAYER_ITERATIONS) or (g.found is TOFIND):
            break

    import IPython; IPython.embed()
    # print 'Number of times not connected: ' + str(notConnected)

    n = len(netlist)
    print 'number of graphs with ' + str(m) + ': ' + str(len(glist))

    if O:
        # Hillclimber session
        for m in range(len(glist)):
            iterations = 0
            found = g.found
            g = copy.deepcopy(glist[m])
            print 'Starting hillclimber'
            print 'Paths found at start hillclimber session: ' + str(g.found)
            print 'Number of paths in netlist: ' + str(n)
            while not (found == n) and (iterations <= MAX_HILLCLIMBER):
                gcopy = copy.deepcopy(g)
                nRemovePaths = random.randint(2,15)
                hillclimbers.standardHillClimber(gcopy, n, nRemovePaths)
                iterations += 1
                if gcopy.found > g.found:
                    g = copy.deepcopy(gcopy)
                    found = g.found
                    print 'new: ' + str(found)
                # print 'No improvement: ' + str(gcopy.found)

            # g.totalTime = time.time() - startTime
            # print '\nTotal time: ' + str(g.totalTime) + ' seconds.\n'
            # print str(iterations) + ' iterations'

    # allpaths = [[] for x in range(n)]
    # for i in range(n):
    #     cur = []
    #     for v in g:
    #         if v.path is i + 1:
    #             cur.append(v.id)
    #     allpaths[i] = cur
    # for m in allpaths:
    #     print m

    print 'found: ' + str(found)

    print 'g.found: ' + str(g.found)

    # import IPython; IPython.embed()

    # found.sort()
    # from itertools import groupby
    # foundSorted = [len(list(group)) for key, group in groupby(found)]
    # import matplotlib.pyplot as plt
    # plt.hist(found)
    # import pylab
    # pylab.savefig('run_randomLayer_results_netlist6_61.png')

    # import toThreejs
    # toThreejs.convert(g)

    draw.allVisualization(g, gates, TOFIND)
