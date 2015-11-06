from data.config1 import width, height, gates
import visualizations.array_backed_grid as draw

depth = 8

class Gate:
    def __init__(self, gate_name, gate_x, gate_y):
        self.name = "gate: " + str(gate_name)
        self.x = gate_x
        self.y = gate_y
    def __repr__(self):
        return "%s" % self.name

grid = [[[0 for z in range(depth)] for x in range(width)] for y in range(height)]

def set_gates(gates, grid):
    for gate in gates:
        grid[gate[1]][gate[0]][0] = Gate((gates.index(gate) + 1), gate[0], gate[1])

set_gates(gates, grid)

for x in range(len(grid)):
    print grid[x]

screen = draw.initGrid(width,height)
draw.drawGrid(grid, screen, Gate)

import IPython; IPython.embed()
