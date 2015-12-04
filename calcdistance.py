from core import *
from data.config1 import width as WIDTH, height as HEIGHT, gates
from data.netlist import netlist_1 as netlist


DEPTH = 8
SURF = WIDTH * HEIGHT


# Convert x-y coordinates of gates to their id and disconnect these vertices
# from the graph.
gateList = []
for c in gates:
    gateList.append(c[1] * WIDTH + c[0])

new_netlist = []
for i in netlist:
	new_netlist.append((gateList[i[0]],gateList[i[1]]))

