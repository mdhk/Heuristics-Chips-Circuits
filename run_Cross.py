"""
CHIPS AND CIRCUITS
"""

from core import *
from data.netlist import *
from random import randint

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
INITIALIZE GRAPH and ADD GATES
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

        message = 'Find path between ' + str(n[0]) + ' and ' + str(n[1])
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
        pathlen.append(len(path) - 2)


        if len(path) > 1:
            print p, path
            # print path
            f += 1
        else:
            print '          PATH NOT FOUND '


        p += 1

        # Prepare graph for next search.
        for v in g:
            v.previous = None

    if (f == 0):
        stop = 1
    return stop


"""
SOLVE
"""
# Count costs total
cost = 0    
startTime = time.time()
# Counts found paths 
tp = 0
for i in range(len(new_netlist)):
    random.shuffle(new_netlist)
    stop = solve(g, new_netlist, vertices_shortest_path)
    verticesWithShortestPath(g, pathlen, pathsvert, vertices_shortest_path)
    
    # Initialize visualization.
    screen = draw.initGrid(WIDTH, HEIGHT)
    grid = [[[0 for c in range(DEPTH)] for b in range(WIDTH)] for a in range(HEIGHT)]
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
    
    new_netlist.pop(verticesWithShortestPath.shortest_path)
    cost += len(vertices_shortest_path) + 1
    pathlen = []
    vertices_shortest_path = []
    verticesWithShortestPath.shortest_path = 0
    
    draw.drawGrid(grid, screen, depth)
    
    if (stop == 1):
        break

for i in total_vertices_shortest_path:
    cost += len(i)

elapsedTime = time.time() - startTime
totalTime += elapsedTime

"""
MESSAGES TO USER
"""

print '\nCosts algorithm: ' + str(cost) + '.'
print '\nTotal time: ' + str(totalTime) + ' seconds.'
print '\nSuccesfully connected ' + str(tp) + ' of ' + str(len(netlist)) + ' required paths.'
print '\nSize surface: ' + str(SURF) + '.'
print '\nShowing layer: ' + str(depth)


if V:
    draw.allVisualization(g, gates, TOFIND)
