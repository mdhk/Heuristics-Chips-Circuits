"""
CHIPS AND CIRCUITS
"""

from core import *
from data.config1 import width as WIDTH, height as HEIGHT, gates
from data.netlist import netlist_1 as netlist
<<<<<<< HEAD
from random import randint
=======
>>>>>>> bf8f8d58e9f3e977f8e3cdde53c9e8248d5d9600


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

new_netlist = netlistConvert2(g, netlist, gateList)

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
    stop = 0
    # Disconnects all vertices from the previous computed shortest path.
    for verticeslist in total_vertices_shortest_path:
        disconnectVertex(g, verticeslist)
    for n in new_netlist:

        start = g.vertDict[n[0]]
        target = g.vertDict[n[1]]

        # Allow connections to target gate (but only from non-gates and from
        # vertices without a pre-existing path.
        connectNonGateVertex(g, target.id)

<<<<<<< HEAD
        message = 'Find path between ' + str(n[0]) + ' and ' + str(n[1])
        print(message.rjust(27)),
=======
        # message = 'Find path between ' + str(n[0] + 1) + ' and ' + str(n[1] + 1)
        # print(message.rjust(27)),
>>>>>>> bf8f8d58e9f3e977f8e3cdde53c9e8248d5d9600


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
        pathlen.append(len(path) - 2)


        if len(path) > 1:
<<<<<<< HEAD
            print p, path
=======
            # print path
>>>>>>> bf8f8d58e9f3e977f8e3cdde53c9e8248d5d9600
            f += 1
        # else:
        #     print '          PATH NOT FOUND '


        p += 1

        # Prepare graph for next search.
        for v in g:
            v.previous = None


        # Fill grid for subsequent visualization.
        if len(path) > 1:
            for i in path[1:-1]:
                grid[(i % SURF) / WIDTH][i % WIDTH][i / SURF] = 1
        draw.drawGrid(grid, screen, depth)
<<<<<<< HEAD
    if (f == 0):
        stop = 1
    return stop
    
=======

    # print '\nLength every path: ' + str(pathlen)
    # print 'Succesfully connected ' + str(f) + ' of ' + str(len(netlist)) + ' required paths.'
>>>>>>> bf8f8d58e9f3e977f8e3cdde53c9e8248d5d9600

"""
SOLVE
"""
# Count costs total
c = 0    
startTime = time.time()
tp = 0
for i in range(len(new_netlist)):
    random.shuffle(new_netlist)
    stop = solve(g, new_netlist, vertices_shortest_path)
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

    
    total_vertices_shortest_path.append(vertices_shortest_path)
    for i in total_vertices_shortest_path:
        randColor = (randint(0, 254), randint(0, 255), randint(0, 255))
        for j in range(len(vertices_shortest_path)):
            grid[(vertices_shortest_path[j] % SURF) / WIDTH][vertices_shortest_path[j] % WIDTH][vertices_shortest_path[j] / SURF] = randColor
    
    tp += 1
    
    print '\ntotalvertshortestpath: ' + str(total_vertices_shortest_path)
    new_netlist.pop(verticesWithShortestPath.shortest_path)
    c += len(vertices_shortest_path) + 1
    pathlen = []
    vertices_shortest_path = []
    verticesWithShortestPath.shortest_path = 0
    
    draw.drawGrid(grid, screen, depth)
    print 'stop : ' + str(stop)
    if (stop == 1):
        break



elapsedTime = time.time() - startTime
totalTime += elapsedTime

print '\nCosts algorithm: ' + str(c) + '.'
print '\nTotal time: ' + str(totalTime) + ' seconds.'
# print '\nLength every path: ' + str(pathlen)
print '\nSuccesfully connected ' + str(tp) + ' of ' + str(len(netlist)) + ' required paths.'


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
