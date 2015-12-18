"""
CHIPS AND CIRCUITS

run_Merge.py

Steps:
    while TOFIND paths are not found:
        create graph
        connect every vertex with its neighbor
        disconnect connections to gates
        remove connections to the first neighbors of gates
        randomize netlist
        for each path in the netlist, compute the shortest path using
            - aStar
            - manhattan heuristic
        disconnect connections to nodes in the path
        if TOFIND paths found: break
            - return Graph
            - visualize the network

"""

from core import *
from data.netlist import *
import algorithms
import random

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

DEPTH = 8
SURF = WIDTH * HEIGHT
# Show visualization (V = 1) or not (V = 0)
V = 1
# Selective disconnect gateNeighbors
# If 1, only the number of neighbors equal to the number of paths still to be
# connected to/from a given gate are guaranteed to be unobstructed. 
S = 1
# Initialize variables that never change.
gateList = []
for c in gates:
    gateList.append(c[1] * WIDTH + c[0])

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

    # Disconnect gates. 
    disconnectVertex(g, gateList)
    for i in gateList:
        g.vertDict[i].gate = True
    # import IPython; IPython.embed()

    if S:
        # Compute number of paths per gate.
        pGate = numberOfPaths(netlist, gateList)
        selectedNeighbors = []
        for i in range(len(pGate)):
            cur = g.vertDict[gateList[i]]
            if len(cur.adjacent) < pGate[i]:
                selectedNeighbors.append([])
                continue
            selectedNeighbors.append(random.sample(cur.adjacent, pGate[i]))
            disconnectVertex(g, selectedNeighbors[i])
    else:
        # Diconnect all neighbors of gates.
        for i in gateList:
            neighbors = computeNeighbors(g, i)
            disconnectVertex(g, neighbors)

    # Mark different paths with p
    p = 1
    # Count found paths
    f = 0
    # Count costs total
    c = 0
    totalTime = 0
    # Keep track of what nodes have 'started' in a path
    startList = []

    """
    SOLVE
    """

    for n in netlist:
        startTime = time.time()

        start = g.vertDict[gateList[n[0]]]
        target = g.vertDict[gateList[n[1]]]

        # Allow connections to target gate (but only from non-gates and from
        # vertices without a pre-existing path.
        connectVertex(g, target.id)

        # Allow connections to neighbors of the target and start gates,
        # exept from nodes with a path
        for nb in computeNeighbors(g, start.id):
            if not g.vertDict[nb].path and not g.vertDict[nb].gate:
                connectNonPathVertex(g, nb)
        for nb in computeNeighbors(g, target.id):
            if not g.vertDict[nb].path and not g.vertDict[nb].gate:
                connectNonPathVertex(g, nb)

        # Use algorithm to compute a path between start and target.
        # start = algorithms.toLowestLayer(g, start)
        # path = []
        # path.append(start.id)
        # tracePath(g, start, path)
        # disconnectVertex(g, path)

        # Compute path between start and target.
        algorithms.aStar(g, start, target)

        # Extract the previously computed path from graph g
        path = []
        path.append(target.id)
        tracePath(g, target, path)

        # Disconnect connections to the vertices in path
        disconnectVertex(g, path)

        # Assign all vertices in the path (not the gates) the path id 
        for i in path[1:-1]:
            g.vertDict[i].path = p
        p += 1

        # Disconnect connections to specific neighbors of start and target
        if S:
            pGate[n[0]] -= 1
            if pGate[n[0]]:
                disconnectVertex(g, selectedNeighbors[gateList.index(start.id)])
            pGate[n[1]] -= 1
            if pGate[n[1]]:
                disconnectVertex(g, selectedNeighbors[gateList.index(target.id)])
        else:
            disconnectVertex(g, computeNeighbors(g, start.id))
            disconnectVertex(g, computeNeighbors(g, target.id))

        g.paths[p] = path

        if len(path) > 1:
            f += 1
            c += len(path) - 1

        # Prepare graph for next search.
        for v in g:
            v.previous = None
    
    # import IPython; IPython.embed()
    g.cost = 0
    for v in g:
        if v.path and not v.gate:
            g.cost += 1
    g.found = f

    return g

if __name__ == "__main__":
    startTime = time.time()

    MAX_ITERATIONS = 2000
    found = []
    m, iterations, found, cost = 0, 0, [], []
    while True:
        iterations += 1
        g = run()
        found.append(g.found)
        cost.append(g.cost)
        if g.found > m:
            # found.append(g.found)
            print 'Current max: ' + str(g.found) + 'paths '
            m = g.found
        if g.found is TOFIND:
        # if iterations >= MAX_ITERATIONS:
            break

    # import pickle
    # with open('mergeNL1_2000Cost.pkl', 'wb') as output:
    #     pickle.dump(cost, output, pickle.HIGHEST_PROTOCOL)
    # with open('mergeNL1_2000Found.pkl', 'wb') as output:
    #     pickle.dump(found, output, pickle.HIGHEST_PROTOCOL)
    import IPython; IPython.embed()

    g.totalTime = time.time() - startTime
    print '\nTotal time: ' + str(g.totalTime) + ' seconds.\n'
    for p in g.paths:
        print g.paths[p]

    draw.allVisualization(g, gates, TOFIND)




    # # Initialize visualization.
    # screen = draw.initGrid(WIDTH, HEIGHT)
    # grid = [[[0 for c in range(DEPTH)] for b in range(WIDTH)] for a in range(HEIGHT)]
    # # Color all gates bright red.
    # for i in gates:
    #     grid[i[1]][i[0]][0] = (255, 0, 0)
    # depth = 0 

    # for p in g.paths:
    #     for i in g.paths[p][1:-1]:
    #         grid[(i % SURF) / WIDTH][i % WIDTH][i / SURF] = 1
    #     # Onhandig dat dit elke keer moet worden geroepen, maar dat komt
    #     # omdat de kleur per call elke keer 1x random wordt beslist. 
    #     draw.drawGrid(grid, screen, depth)

    # # import IPython; IPython.embed()
    # while True:
    #     event = pygame.event.wait()
    #     if event.type == pygame.QUIT:
    #         pygame.quit()
    #     elif event.type == pygame.MOUSEBUTTONDOWN:
    #         # Visualize the layer up or down from current (left and right click
    #         # respectively).
    #         if event.button == 1 and depth != 7:
    #             screen.fill([255,255,255])
    #             depth += 1
    #             draw.drawGrid(grid, screen, depth)
    #             print 'Showing layer: ' + str(depth)
    #         if event.button == 3 and depth != 0:
    #             screen.fill([255,255,255])
    #             depth -= 1
    #             draw.drawGrid(grid, screen, depth)
    #             print 'Showing layer: ' + str(depth)

#     results.sort()
#     from itertools import groupby
#     resultsSorted = [len(list(group)) for key, group in groupby(results)]
#     import matplotlib.pyplot as plt
#     plt.hist(results)
#     import pylab
#     pylab.savefig('pathsfound.png')

