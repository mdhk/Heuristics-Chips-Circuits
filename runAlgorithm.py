"""
CHIPS AND CIRCUITS
"""

from core import *
from data.config1 import width as WIDTH, height as HEIGHT, gates
from data.netlist import netlist_1 as netlist
from algorithms import aStar as algorithm

DEPTH = 8
SURF = WIDTH * HEIGHT

"""
INITIALIZE GRAPH AND VISUALIZATION
"""

# to debug some function, use this:
# import IPython;
# IPython.embed(); 


# Create graph and connect it.
g = Graph(WIDTH, HEIGHT, DEPTH, SURF)
connectGraph(g)

# Convert x-y coordinates of gates to their id and disconnect these vertices
# from the graph.
gateList = []
for c in gates:
    gateList.append(c[1] * WIDTH + c[0])
disconnectVertex(g, gateList)
for i in gateList:
    g.vertDict[i].gate = True

random.shuffle(netlist)

z = mostConnexionNetlist(g, netlist, gateList)
    


"""
to run program with netlist ordered from short to long
"""
# a = netlistConvert2(g, netlist, gateList)
# b = netlistCalcDist(g, a)
# newnet = short2longNetlist(a, b)




# Mark different paths with p
p = 0
# Count found paths
f = 0
# Count costs total
c = 0
totalTime = 0

# Initialize visualization.
screen = draw.initGrid(WIDTH, HEIGHT)
grid = [[[0 for c in range(DEPTH)] for b in range(WIDTH)] for a in range(HEIGHT)]
# Color all gates bright red.
for i in gates:
    grid[i[1]][i[0]][0] = (255, 0, 0)

depth = 0 

"""
SOLVE
"""



for n in z:
    startTime = time.time()
    start = n[0]
    target = n[1]
    print "target:" + str(target)
    # Allow connections to target gate (but only from non-gates and from
    # vertices without a pre-existing path.
    connectVertex(g, target)

    message = 'Find path between ' + str(n[0] + 1) + ' and ' + str(n[1] + 1)
    print(message.rjust(27)),

    # Use algorithm to compute a path between start and target.
    algorithm(g, g.vertDict[start], g.vertDict[target])

    # Extract the previously computed path from graph g
    path = []
    path.append(target)
    tracePath(g, g.vertDict[target], path)

    # Disconnect connections to the vertices in path
    disconnectVertex(g, path)

    # Assign all vertices in the path (not the gates) the path id 
    for i in path[1:-1]:
        g.vertDict[i].path = p
    p += 1

    if len(path) > 1:
        print path
        f += 1
        c += len(path) - 1
    else:
        print '          PATH NOT FOUND '

    # Prepare graph for next search.
    for v in g:
        v.previous = None

    # Fill grid for subsequent visualization.
    if len(path) > 1:
        for i in path[1:-1]:
            grid[(i % SURF) / WIDTH][i % WIDTH][i / SURF] = 1
    draw.drawGrid(grid, screen, depth)

    elapsedTime = time.time() - startTime
    totalTime += elapsedTime

print '\nTotal time: ' + str(totalTime) + ' seconds.'
print '\nCosts algorithm: ' + str(c) + '.'
print '\nSuccesfully connected ' + str(f) + ' of ' + str(len(netlist)) + '\
 required paths.'
print '\nSize surface: ' + str(SURF) + '.'
print '\nShowing layer: ' + str(depth)




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
