"""
CHIPS AND CIRCUITS
"""

from core import *

"""
INITIALIZE GRAPH AND VISUALIZATION
"""

# Create graph and connect it.
g = Graph()
connectGraph(g)

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

# Initialize visualization.
screen = draw.initGrid(WIDTH, HEIGHT)
grid = [[[0 for c in range(DEPTH)] for b in range(WIDTH)] for a in range(HEIGHT)]
# Color all gates bright red.
for i in gates:
    grid[i[1]][i[0]][0] = (255, 0, 0)


path = []
depth = 0 

# import IPython; IPython.embed()

"""
SOLVE
"""

random.shuffle(netlist)
for n in netlist:
    startTime = time.time()

    start = g.vertDict[gateList[n[0]]]
    target = g.vertDict[gateList[n[1]]]
    # Connect start and target gates.
    for i in start.adjacent:
        g.vertDict[i].addNeighbor(gateList[n[0]])
    for i in target.adjacent:
        g.vertDict[i].addNeighbor(gateList[n[1]])

    # Find path.
    message = 'Find path between ' + str(n[0] + 1) + ' and ' + str(n[1] + 1)
    print(message.rjust(27)),

    algorithm(g, start, target, p)

    path = applyPath(g, target.id, start.id, p)
    p += 1
    if len(path) is not 1:
        print path
        f += 1
        c += len(path) - 1
    else:
        print '          PATH NOT FOUND '

    if len(path) > 1:
        for i in path[1:-1]:
            grid[(i % SURF) / WIDTH][i % WIDTH][i / SURF] = 1

    draw.drawGrid(grid, screen, depth)

    elapsedTime = time.time() - startTime
    totalTime += elapsedTime
    # print 'Time: ' + str(elapsedTime)

print '\n\nTotal time: ' + str(totalTime) + ' seconds.'
print '\n\nCosts algorithm: ' + str(c)
print '\n\nSuccesfully connected ' + str(f) + ' of ' + str(len(netlist)) + '\
 required paths.'
print SURF


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


