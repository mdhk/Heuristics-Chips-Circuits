"""
CHIPS AND CIRCUITS

run_randomLayer.py

Steps:
    Note: paths cannot go over gates or other paths.

    while TOFIND paths are not found and iterations < MAX_LAYER_ITERATIONS:
        Randomize netlist.
        For all gates, if the number of required paths == the number of free
            neighbors, reserve all neighbors to that gate and update the
            start/target positions for each path to those neighbors.
        For each netlist pair, compute the path to a single randomly chosen
            layer l (between 0 and 7). Update the netlist to the two vertices in l.
        Disconnect the immediate neighbors of all vertices in the netlist.
        Iterating over each pair in the netlist:
            Reconnect the immediate neighbors of the two vertices.
            Find the shortest path between these two vertices.
        Because in the first iteration an abundance of vertices may have been
            disconnected, repeat the previous iterations once more for those paths
            not yet found.

    if not found TOFIND paths:
        Hillclimber

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

    # Initialize found, time.
    g.found, totalTime = 0,0
    # Newnetlist will keep track of the 'new' positions of start/target
    # vertices of paths.
    newnetlist = copy.deepcopy(netlist)
    netlistMH = netlistManhattan(g, netlist)

    # For each starting/target vertex, if the number of paths they are part of == number of free
    # neighbors, reserve each neighbor for a specific path.
    for iter in range(5):
    
        # Number of paths to find per vertex in newnetlist.
        nPaths = numberOfPathsDict(newnetlist)
        # Number of 'free' neighbors per start/target vertex.
        nNonGateNeighbors = nonGatePathNeighbors(g, nPaths)
        for n in nPaths:
            if nPaths[n] == nNonGateNeighbors[n]:
                pathNumber, index = [], []
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
                for i in ind:
                    g.vertDict[nb[i]].path = pathNumber[i]
                    newnetlist[pathNumber[i]-1][index[i]] = nb[i]
                disconnectVertex(g, nb)

    netlistMH = netlistManhattan(g, newnetlist)

    # For each netlist pair, create a path to the same random layer. 
    for i in range(N):
        if netlistMH[i] > MIN_MANHATTAN:

            # Choose random layer.
            l = random.choice(range(0, 8))
            # List vertices in layer 'l'.
            lVertices = range(g.SURF * l, g.SURF * (l + 1))

            cur = g.vertDict[newnetlist[i][0]]
            foundFirst = algorithms.aStarList(g, cur, lVertices, g.vertDict[cur.id - g.SURF * cur.z + g.SURF * l])
            if not foundFirst:
                for v in g:
                    v.previous = None
                # If no path from layer 0 to layer l was found, continue with
                # next netlist iteration.
                continue
            else:
                pathFirst = []
                pathFirst.append(foundFirst)
                tracePath(g, g.vertDict[foundFirst], pathFirst)
                for v in g:
                    v.previous = None

            cur = g.vertDict[newnetlist[i][1]]
            foundSecond = algorithms.aStarList(g, cur, lVertices, g.vertDict[cur.id - g.SURF * cur.z + g.SURF * l])
            if not foundSecond:
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
    # all start/target vertices.
    if D:
        for i in newnetlist:
            disconnectVertex(g, computeNeighbors(g, i[0]))
            disconnectVertex(g, computeNeighbors(g, i[1]))

    g.newnetlist = copy.deepcopy(newnetlist)

    # Try to find the complete path list twice (some neighbors of
    # starting/target vertices might be disconnected on the first iteration but
    # connected on the second iteration.
    if D:
        rounds = 2
    else:
        rounds = 1

    for x in range(rounds):

        # EXPERIMENTAL
        # If there are paths reserved but not used, remove them.
        if x == 1:
            for i in range(N):
                if not g.connectedPaths[i]:
                    # print (i + 1)
                    for v in g:
                        if v.path == (i + 1):
                            v.path = 0
            for v in g:
                if not v.path and not v.gate:
                    connectVertex(g, v.id)
            for i in range(N):
                if g.connectedPaths[i]:
                    newnetlist[i] = [0, 0]
        # EXPERIMENTAL END

        # Find paths between the (updated) netlist vertex pairs.
        p = 0
        for n in newnetlist:
            p += 1
            if n == [0, 0]:
                continue
            start = g.vertDict[n[0]]
            target = g.vertDict[n[1]]

            # Reconnect neighbors of start and target vertex.
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
                g.connectedPaths[p - 1] = True

            # Assign all vertices in the path (not the gates) the path id 
            for i in path:
                cur = g.vertDict[i]
                if not cur.gate:
                    cur.path = p

            # Prepare graph for next search.
            for v in g:
                v.previous = None

            # # EXPERIMENTAL
            # # Make sure there are no redundant vertices in the path
            # gtemp = copy.deepcopy(g)
            # pathlist = []
            # for v in gtemp:
            #     if v.path == p:
            #         pathlist.append(v.id)

            # disconnectVertex(g, range(v.id))
            # for v in gtemp: 
            #     if v.id in pathlist:
            #         for nb in computeNeighbors(g, v.id):
            #             if nb in pathlist:
            #                 v.addNeighbor()
            #         disconnectVertex(g, [v.id])

            # import IPython; IPython.embed()

            # pathlist = []
            # for v in g:
            #     if v.path == p:
            #         pathlist.append(v.id)
            #         connectVertex(g, v.id)
            #     else:
            #         disconnectVertex(g, [v.id])

            # nl = netlist[p-1]
            # connectVertex(g, nl[1])
            # algorithms.aStar(g, g.vertDict[nl[0]], g.vertDict[nl[1]])
            # path = []
            # path.append(nl[1])
            # tracePath(g, g.vertDict[nl[1]], path)
            # disconnectVertex(g, path)

            # for v in g:
            #     if not v.path and not v.gate:
            #         connectVertex(g, v.id)
            #     else:
            #         disconnectVertex(g, [v.id])
            # import IPython; IPython.embed()

            # # EXPERIMENTAL END

    g.cost = 0
    for v in g:
        if v.path:
            g.cost += 1

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

    MAX_LAYER_ITERATIONS = 10000
    MAX_HILLCLIMBER = 1000
    # 2 OR 3?
    MIN_MANHATTAN = 4

    DEPTH = 8
    SURF = WIDTH * HEIGHT
    # Show visualization (V = 1) or not (V = 0)
    V = 1
    # Disconnect neighbors # WERKT AVERECHTS
    D = 0
    # Optimize after initial run() (Hillclimber)
    O = 0
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
        found.append(g.found)
        if g.found > m:
            glist = []
            m = g.found
            # # Save newly (max) found object as ..pkl
            # with open('randomLayerNL6_Nfound6.pkl', 'wb') as output:
            #     pickle.dump(g, output, pickle.HIGHEST_PROTOCOL)
        if (g.found == m):
            glist.append(copy.deepcopy(g))
            print 'Newly found: ' + str(m) + ', ' + str(len(glist)) + ' times.'

        if (g.found is TOFIND) or (iterations >= MAX_LAYER_ITERATIONS):
        # if (g.found >= 65): #or (iterations >= MAX_LAYER_ITERATIONS):
        # if (iterations >= MAX_LAYER_ITERATIONS):
            break

    print 'number of graphs with ' + str(m) + ': ' + str(len(glist))

    if O:
        # Hillclimber session
        for m in range(len(glist)):
            iterations = 0
            found = g.found
            g = copy.deepcopy(glist[m])
            print 'Starting hillclimber'
            print 'Paths found at start hillclimber session: ' + str(g.found)
            print 'Number of paths in netlist: ' + str(N)
            while not (found == N) and (iterations <= MAX_HILLCLIMBER):
                gcopy = copy.deepcopy(g)
                nRemovePaths = random.randint(2,15)
                hillclimbers.standardHillClimber(gcopy, N, nRemovePaths)
                iterations += 1
                if gcopy.found > g.found:
                    g = copy.deepcopy(gcopy)
                    found = g.found
                    print 'new: ' + str(found)

    print 'found: ' + str(found)
    print 'g.found: ' + str(g.found)

    # Output checker

    # g = glist.pop()
    # pathsfound = []
    # for i in range(N):
    #     path = []
    #     cur = g.netlist[i][0]
    #     target = g.netlist[i][1]
    #     complete = False
    #     # import IPython; IPython.embed()
    #     # while not complete:
    #     iterations = 0
    #     while not complete and not (iterations == 10000):
    #         iterations += 1
    #         for nb in computeNeighbors(g, cur):
    #             if nb == target:
    #                 path.append(nb)
    #                 # print path
    #                 complete = True
    #                 pathsfound.append(i + 1)
    #             if g.vertDict[nb].path is (i + 1) and nb not in path:
    #                 # print nb
    #                 path.append(nb)
    #                 cur = nb
    #         # import IPython; IPython.embed()
    #     # print path
    #     # print pathsfound

    # import IPython; IPython.embed()

    """
    VISUALIZATIONS
    """

    # Frequency chart of solutions per iteration. 

    # found.sort()
    # from itertools import groupby
    # foundSorted = [len(list(group)) for key, group in groupby(found)]
    # import matplotlib.pyplot as plt
    # plt.hist(found)
    # import pylab
    # pylab.savefig('frequencyBar.png')

    # Frequency chart of solutions per iteration, with normal fitted.

    import numpy as np
    from scipy.stats import norm
    import matplotlib.pyplot as plt
    data = found
    mu, std = norm.fit(data)
    plt.hist(data, bins=25, normed=True, alpha=0.6, color='g')
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth = 2)
    title = "Fit results: mu = %.2f, std = %.2f" % (mu, std)
    plt.title(title)
    import pylab
    pylab.savefig('frequencyBarNormDist.png')

    # Save jsonThreejs.json file (based on g) for 3D visualization.
    
    import toThreejs
    toThreejs.convert(g)

    # import IPython; IPython.embed()

    # Draw 2D visualization.

    draw.allVisualization(g, gates, TOFIND)
