"""
CHIPS AND CIRCUITS
"""

from core import *
from data.config1 import width as WIDTH, height as HEIGHT, gates
from data.netlist import netlist_2 as netlist
import algorithms

DEPTH = 8
SURF = WIDTH * HEIGHT

"""
INITIALIZE GRAPH AND VISUALIZATION
"""

def run_aStarManhattan_Many():
    V = 1

    # Create graph and connect it.
    g = Graph(WIDTH, HEIGHT, DEPTH, SURF)
    connectGraph(g)
    g.SURF = SURF
    g.WIDTH = WIDTH
    g.HEIGHT = HEIGHT

    # Convert x-y coordinates of gates to their id and disconnect these vertices
    # from the graph.
    gateList = []
    for c in gates:
        gateList.append(c[1] * WIDTH + c[0])
    disconnectVertex(g, gateList)
    for i in gateList:
        g.vertDict[i].gate = True

    # Mark different paths with p
    p = 0
    # Count found paths
    f = 0
    # Count costs total
    c = 0
    totalTime = 0

    if V:
        # Initialize visualization.
        screen = draw.initGrid(WIDTH, HEIGHT)
        grid = [[[0 for c in range(DEPTH)] for b in range(WIDTH)] for a in range(HEIGHT)]
        # Color all gates bright red.
        for i in gates:
            grid[i[1]][i[0]][0] = (255, 0, 0)
        depth = 0 

    random.shuffle(netlist)
    # Check manhattan distance of netlist
    # manhattanNetlist = []
    # for n in netlist:
    #     manhattanNetlist.append(algorithms.normalManhattan(g.vertDict[gateList[n[0]]], \
    #         g.vertDict[gateList[n[1]]]))

    # import IPython; IPython.embed()




    # Keep track of what nodes have 'started' in a path
    startList = []

    """
    SOLVE
    """

    for n in netlist:
        if V:
            startTime = time.time()

        start = g.vertDict[gateList[n[0]]]
        target = g.vertDict[gateList[n[1]]]

        if start.id in startList and target.id not in startList:
            tmp = start
            start = target
            target = start

        # Allow connections to target gate (but only from non-gates and from
        # vertices without a pre-existing path.
        connectVertex(g, target.id)


        # Use algorithm to compute a path between start and target.
        start = algorithms.toLowestLayer(g, start)
        path = []
        path.append(start.id)
        tracePath(g, start, path)
        disconnectVertex(g, path)
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

        if V:
            message = 'Find path between ' + str(n[0] + 1) + ' and ' + str(n[1] + 1)
            print(message.rjust(27)),

        if len(path) > 1:
            if V:
                print path
            f += 1
            c += len(path) - 1
        else:
            if V:
                print '          PATH NOT FOUND '
            None

        # Prepare graph for next search.
        for v in g:
            v.previous = None

        if V:
            # Fill grid for subsequent visualization.
            if len(path) > 1:
                for i in path[1:-1]:
                    grid[(i % SURF) / WIDTH][i % WIDTH][i / SURF] = 1
            draw.drawGrid(grid, screen, depth)
            elapsedTime = time.time() - startTime
            totalTime += elapsedTime
    import IPython; IPython.embed()

    if V:
        print '\n\nTotal time: ' + str(totalTime) + ' seconds.'
        print '\n\nCosts algorithm: ' + str(c)
        print '\n\nSuccesfully connected ' + str(f) + ' of ' + str(len(netlist)) + '\
        required paths.'
        # Wait for mouse click to close visualization or view other layer
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Visualize the layer up or down from current (left and right click
                # respectively).
                if event.button == 1:
                    screen.fill([255,255,255])
                    depth += 1
                    draw.drawGrid(grid, screen, depth)
                if event.button == 3:
                    screen.fill([255,255,255])
                    depth -= 1
                    draw.drawGrid(grid, screen, depth)
                print 'Showing layer: ' + str(depth)

    return f

if __name__ == "__main__":
    startTime = time.time()
    results = []
    for i in range(1):
        results.append(run_aStarManhattan_Many())
    import IPython; IPython.embed()
    print '\n\nTotal time: ' + str(time.time() - startTime) + ' seconds.'

    results.sort()
    from itertools import groupby
    resultsSorted = [len(list(group)) for key, group in groupby(results)]
    import matplotlib.pyplot as plt
    plt.hist(results)
    import pylab
    pylab.savefig('aStarWeirdManhattan_Many_PathsFound.png')
    import IPython; IPython.embed()
