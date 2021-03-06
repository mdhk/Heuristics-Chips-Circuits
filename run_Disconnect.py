"""
CHIPS AND CIRCUITS

run_Merge.py

Steps:
    while TOFIND paths are not found:
        create graph
        connect every vertex with its neighbor
        disconnect connections to gates
        randomize netlist
        remove connections to selected first neighbors of gates
        for each path in the netlist, compute the shortest path using
            - aStar(manhattan heuristic)
        disconnect connections to nodes in the path
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
        pGate[n[0]] -= 1
        if pGate[n[0]]:
            disconnectVertex(g, selectedNeighbors[gateList.index(start.id)])
        pGate[n[1]] -= 1
        if pGate[n[1]]:
            disconnectVertex(g, selectedNeighbors[gateList.index(target.id)])

        g.paths[p] = path

        if len(path) > 1:
            f += 1

        # Prepare graph for next search.
        for v in g:
            v.previous = None
    
    g.cost = 0
    for v in g:
        if v.path and not v.gate:
            g.cost += 1
    g.found = f

    return g

if __name__ == "__main__":
    startTime = time.time()

    MAX_ITERATIONS = 500
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
        if g.found is TOFIND or iterations >= MAX_ITERATIONS:
            break


    g.totalTime = time.time() - startTime
    print '\nTotal time: ' + str(g.totalTime) + ' seconds.\n'
    for p in g.paths:
        print g.paths[p]
    print 'costs: ' + str(g.cost)

    if V:
        draw.allVisualization(g, gates, TOFIND)