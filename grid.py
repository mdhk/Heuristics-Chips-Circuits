from data.testData import width, height, gates
import visualizations.array_backed_grid as draw

depth = 8

class Vertex:
    def __init__(self, vertex_label='', gate_x='', gate_y=''):
        self.name = str(vertex_label)
    def __repr__(self):
        return "%s" % self.name

# class PriorityQueue:
#     def __init__(self):
#         self.queue = []

grid = [[[Vertex() for z in range(depth)] for x in range(width)] for y in range(height)]

def set_gates(gates, grid):
    for gate in gates:
        grid[gate[1]][gate[0]][0] = Vertex((gates.index(gate) + 1))

set_gates(gates, grid)

# for x in range(len(grid)):
#     print grid[x]

screen = draw.initGrid(width,height)
draw.drawGrid(grid, screen, depth)

import IPython; IPython.embed()
