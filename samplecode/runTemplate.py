"""
CHIPS AND CIRCUITS
"""

from core import *
from data.config1 import width as WIDTH, height as HEIGHT, gates
from data.netlist import netlist_1 as netlist
import algorithms

DEPTH = 8
SURF = WIDTH * HEIGHT
# Show visualization (V = 1) or not (V = 0).
V = 1

# Initialize variables that never change.
gateList = []
for c in gates:
    gateList.append(c[1] * WIDTH + c[0])

def run():
    # Create graph and connect it.
    g = Graph(WIDTH, HEIGHT, DEPTH, SURF)
    connectGraph(g)
    g.SURF = SURF
    g.WIDTH = WIDTH
    g.HEIGHT = HEIGHT

    # Disconnect connections to gates.
    disconnectVertex(g, gateList)
    for i in gateList:
        g.vertDict[i].gate = True

    """
    SOLVE
    Notes:
    To compute a path, the target gate need to be 'connected'. That is,
    connections to the target gate should be restored: connectVertex(g,target.id).
    """

    for n in netlist:
        # DO THINGS
        return

    return numberOfFoundPaths

if __name__ == "__main__":
    startTime = time.time()

    results = []

    for i in range(1):
        results.append(run())

    print '\n\nTotal time: ' + str(time.time() - startTime) + ' seconds.'

    # Create a frequency bar chart displaying the number of paths found. 
    results.sort()
    from itertools import groupby
    resultsSorted = [len(list(group)) for key, group in groupby(results)]
    import matplotlib.pyplot as plt
    plt.hist(results)
    import pylab
    pylab.savefig('numberOfPathsFound.png')
    import IPython; IPython.embed()
