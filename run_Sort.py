"""
CHIPS AND CIRCUITS
"""
# to debug some function, use this:
# import IPython;
# IPython.embed();

from core import *
from data.netlist import *
from algorithms import aStar as algorithm

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


"""
VARIABLES and STRINGS
"""
DEPTH = 8
SURF = WIDTH * HEIGHT

# Show visualization (V = 1) or not (V = 0)
V = 1
# Mark different paths with p
p = 0
# Count found paths
f = 0
# Count costs total
cost = 0
mincost = 0
depth = 0 
totalTime = 0


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

print "gates: " + str(gateList)


"""
Netlist sorting methods
"""
random.shuffle(netlist)

a = netlistConvert2(g, netlist, gateList)
b = netlistCalcDist(g, a)


# comment out to use netlist with most connexions first
# newnet = mostConnexionNetlist(g, netlist, gateList)

# comment out to use netlist with longest distance between gates first
# newnet = long2shortNetlist(a, b)

# to run program with netlist ordered from short to long
newnet = short2longNetlist(a, b)


"""
SOLVE
"""
for n in newnet:
    startTime = time.time()
    start = n[0]
    target = n[1]
    
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
        cost += len(path) - 1
    else:
        print '          PATH NOT FOUND '

    # Prepare graph for next search.
    for v in g:
        v.previous = None


    elapsedTime = time.time() - startTime
    totalTime += elapsedTime

print '\nTotal time: ' + str(totalTime) + ' seconds.'
print '\nCosts algorithm: ' + str(cost) + '.'
print '\nSuccesfully connected ' + str(f) + ' of ' + str(len(netlist)) + '\
 required paths.'
print '\nSize surface: ' + str(SURF) + '.'
print '\nShowing layer: ' + str(depth)

if V:
    draw.allVisualization(g, gates, TOFIND)