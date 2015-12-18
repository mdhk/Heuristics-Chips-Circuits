"""
CHIPS AND CIRCUITS
"""

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
c = 0
totalTime = 0
# paths on every vertex
pathsvert = []
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

print "gates: " + str(gateList)


"""
to run program with netlist ordered from short to long
"""
a = netlistConvert2(g, netlist, gateList)
b = netlistCalcDist(g, a)
newnet = short2longNetlist(a, b)



# # Initialize visualization.
# screen = draw.initGrid(WIDTH, HEIGHT)
# grid = [[[0 for c in range(DEPTH)] for b in range(WIDTH)] for a in range(HEIGHT)]
# # Color all gates bright red.
# for i in gates:
#     grid[i[1]][i[0]][0] = (255, 0, 0)

# depth = 0 

"""
SOLVE
"""
print 'newnet: ' + str(newnet)
def main():
    runn(newnet)

def runn(newnet):
    global p, f, c, totalTime
    for n in range(len(newnet)):
        startTime = time.time()
        # import IPython;
        # IPython.embed(); 
        start = newnet[n][0]
        target = newnet[n][1]

        print '\nNewnet: ' + str(newnet)
        
        # Allow connections to target gate (but only from non-gates and from
        # vertices without a pre-existing path.
        connectVertex(g, target)

        message = 'Find path between ' + str(start) + ' and ' + str(target) + ' ' + str(p)
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
            pathsvert[i].append(p)
        

        if len(path) > 1:
            print path
            f += 1
            # c += len(path) - 1
        else:
            print '          PATH NOT FOUND '
            for v in range(len(pathsvert)):
                if (pathsvert[v] == [p-1]):
                    pathsvert[v] = []
                    # grid[(v % SURF) / WIDTH][v % WIDTH][v / SURF] = 0

            if (n ==  0):
                random.shuffle(newnet)
            else:
                newnet = newnet[(n-1):]
                random.shuffle(newnet)            
                p -= 1
            return runn(newnet)
            
        p += 1

        # Prepare graph for next search.
        for v in g:
            v.previous = None

        elapsedTime = time.time() - startTime
        totalTime += elapsedTime

main()


print '\nTotal time: ' + str(totalTime) + ' seconds.'
print '\nCosts algorithm: ' + str(c) + '.'
print '\nSuccesfully connected ' + str(f) + ' of ' + str(len(netlist)) + '\
 required paths.'
print '\nSize surface: ' + str(SURF) + '.'
print '\nShowing layer: ' + str(depth)


if V:
    draw.allVisualization(g, gates, TOFIND)
