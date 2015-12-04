"""
CHIPS AND CIRCUITS
"""

from core import *
from data.config1 import width as WIDTH, height as HEIGHT, gates
from data.netlist import netlist_1 as netlist


DEPTH = 8
SURF = WIDTH * HEIGHT

"""
VARIABLES and STRINGS
"""

totalTime = 0
# netlist with lengths of every path p
pathlen = []
# paths on every vertex
pathsvert = []
shortest_path = 100
# lijst met vertices waar de kortste pad over loopt
vertices_shortest_path = []
total_vertices_shortest_path = []

for i in range(SURF*DEPTH):
    pathsvert.append([])


"""
INITIALIZE GRAPH AND VISUALIZATION
"""
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


# Initialize visualization.
screen = draw.initGrid(WIDTH, HEIGHT)
grid = [[[0 for c in range(DEPTH)] for b in range(WIDTH)] for a in range(HEIGHT)]
# Color all gates bright red.
for i in gates:
    grid[i[1]][i[0]][0] = (255, 0, 0)

depth = 0 



def solve(g,netlist, vertices_shortest_path):
    # Count found paths
    f = 0
    # Mark different paths with p
    p = 0
    # Disconnects all vertices from the previous computed shortest path on the vertex with the most paths.
    disconnectVertex(g, total_vertices_shortest_path)
    for n in netlist:

        start = g.vertDict[gateList[n[0]]]
        target = g.vertDict[gateList[n[1]]]

        # Allow connections to target gate (but only from non-gates and from
        # vertices without a pre-existing path.
        connectNonGateVertex(g, target.id)

        message = 'Find path between ' + str(n[0] + 1) + ' and ' + str(n[1] + 1)
        print(message.rjust(27)),


        # Use algorithm to compute a path between start and target.
        algorithm(g, start, target)

        # Extract the previously computed path from graph g
        path = []
        path.append(target.id)
        tracePath(g, target, path)

        # Assign all vertices in the path (not the gates) the path id 
        for i in path[1:-1]:
            g.vertDict[i].path = p
            pathsvert[i].append(p)
        p += 1
        pathlen.append(len(path) - 2)


        if len(path) > 1:
            print path
            f += 1
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

    # print '\nLength every path: ' + str(pathlen)
    print '\nSuccesfully connected ' + str(f) + ' of ' + str(len(netlist)) + ' required paths.'

"""
SOLVE
"""
# Count costs total
c = 0    
startTime = time.time()
for i in range(len(netlist)):
    solve(g, netlist, vertices_shortest_path)
    verticesWithShortestPath(g, pathlen, pathsvert, vertices_shortest_path)

    # Initialize visualization.
    screen = draw.initGrid(WIDTH, HEIGHT)
    # Color all gates bright red.
    for i in gates:
        grid[i[1]][i[0]][0] = (255, 0, 0)

    depth = 0 

    for v in range(len(pathsvert)):
        if (pathsvert[v] != []):
            pathsvert[v] = []
            grid[(v % SURF) / WIDTH][v % WIDTH][v / SURF] = 0

    for j in range(len(vertices_shortest_path)):
        total_vertices_shortest_path.append(vertices_shortest_path[j])
        grid[(vertices_shortest_path[j] % SURF) / WIDTH][vertices_shortest_path[j] % WIDTH][vertices_shortest_path[j] / SURF] = 1
    c += len(vertices_shortest_path) + 1
    netlist.pop(verticesWithShortestPath.shortest_path)

    draw.drawGrid(grid, screen, depth)


elapsedTime = time.time() - startTime
totalTime += elapsedTime

print '\nCosts algorithm: ' + str(c) + '.'
print '\nTotal time: ' + str(totalTime) + ' seconds.'


"""
MESSAGES TO USER
"""

print '\nSize surface: ' + str(SURF) + '.'
print '\nShowing layer: ' + str(depth)


"""
HANDLE EVENTS
"""

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
