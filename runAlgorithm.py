"""
CHIPS AND CIRCUITS
"""

from core import *
from data.config1 import width, height, gates
from data.netlist import netlist_2 as netlist
from Algorithms import aStar

WIDTH = width
HEIGHT = height
SURF = width * height
DEPTH = 8
depth = 0

g = Graph()
connect_Graph(g)

gateList = []
for c in gates:
    # In config1, coordinates are [x, y]
    # ONLY FOR PRINT 1
    gateList.append(c[1] * WIDTH + c[0])

# Disconnect gates
disconnect_vertex(g, gateList)
for i in gateList:
    g.vert_dict[i].gate = True

# Find shortest path between the gates in the netlist
# Mark different paths with p
p = 0
total_time = 0

# Init visualization.
screen = draw.initGrid(WIDTH, HEIGHT)
grid = [[[0 for c in range(DEPTH)] for b in range(WIDTH)] for a in range(HEIGHT)]

path = []
for n in netlist:
    start_time = time.time()

    begin = g.vert_dict[gateList[n[0]]]
    end = g.vert_dict[gateList[n[1]]]
    # Connect begin and end gates.
    for i in begin.adjacent:
        g.vert_dict[i].add_neighbor(gateList[n[0]])
    for i in end.adjacent:
        g.vert_dict[i].add_neighbor(gateList[n[1]])

    # Find path.
    print 'Find path between ' + str(n[0] + 1) + ' and ' + str(n[1] + 1)
    ############################
    # Choose algorithm and find shortest path between start and target node
    ############################
    # dijkstra(g, begin, end)
    aStar(g, begin, end)
    # bfs(g, begin, end)

    path = apply_path(g, end.id, begin.id, p)
    p += 1

    if len(path) > 1:
        for i in path:
            grid[(i % (WIDTH * HEIGHT))/WIDTH][i % WIDTH][i/(WIDTH * HEIGHT)] = 1

    draw.drawGrid(grid, screen, depth)

    elapsed_time = time.time() - start_time
    total_time += elapsed_time
    print 'time: ' + str(elapsed_time)

print 'total time: ' + str(total_time)

# import IPython; IPython.embed();

while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        # User clicks the mouse. Go to the next layer
        screen.fill([255,255,255])
        depth = depth + 1
        draw.drawGrid(grid, screen, depth)