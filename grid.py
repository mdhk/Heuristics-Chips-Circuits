from data.testData import width, height, gates
import visualizations.array_backed_grid as draw

depth = 8

class Vertex:
    goal = gate_goal
    def __init__(self, vertex_label='', gate_x='', gate_y=''):
        self.name = str(vertex_label)
        self.x = gate_x
        self.y = gate_y
    def __repr__(self):
        return "%s" % self.name
    def add_goal(self, goal):
        self.goal = gate_goal

grid = [[[Vertex() for z in range(depth)] for x in range(width)] for y in range(height)]

def set_gates(gates, grid):
    for gate in gates:
        startgate = [pair[0] for pair in netlist].index(gate[0])
        endgatelist = [pair[1] for pair in netlist]
        gate_goal = endgatelist[startgate]
        grid[gate[1]][gate[0]][0] = Vertex((gates.index(gate) + 1), gate[0], gate[1])

set_gates(gates, grid)

for x in range(len(grid)):
    print grid[x]

screen = draw.initGrid(width,height)
for i in range(depth):
    draw.drawGrid(grid, screen, i)

import IPython; IPython.embed()
