# Adapted from:
# http://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php.

import sys, time

class Vertex:
    def __init__(self, id):
        self.id = id
        self.adjacent = {}
        self.distance = sys.maxint
        self.visited = False
        self.previous = None
        self.path = None
        self.gate = False

    def add_neighbor(self, neighbor, weight = 1):
        self.adjacent[neighbor] = weight

    def set_distance(self, dist):
        self.distance = dist

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, id):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(id)
        self.vert_dict[id] = new_vertex
        return new_vertex

# Calculate shortest path from a given node v.
# Can be called after dijkstra finished for a given start-end pair of vertices.
def shortest(v, path):
    if v.previous:
        path.append(v.previous.id)
        shortest(v.previous, path)
        return

import heapq

def dijkstra(aGraph, start, target):
    # DEBUG
    # distance = [0 for i in range(40)]

    start.set_distance(0)

    unvisited_queue = [(v.distance, v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    # DEBUG
    # import IPython; IPython.embed()

    while len(unvisited_queue):
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # import IPython; IPython.embed()

        # # DEBUG
        # distance[current.distance] += 1
        # print distance

        for next in current.adjacent:
            next = aGraph.vert_dict[next]
            if next.visited:
                continue
            new_dist = current.distance + 1

            if new_dist < next.distance:
                next.set_distance(new_dist)
                next.set_previous(current)

        # DEBUG
        # import IPython; IPython.embed()
        
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        unvisited_queue = [(v.distance, v) for v in aGraph if not
                v.visited]
        heapq.heapify(unvisited_queue)

        # When target has been visited, break
        if target.visited:
            break

def disconnect_vertex(aGraph, v):
    surf = WIDTH * HEIGHT
    for i in v:
        a = i % surf
        if (i >= surf and aGraph.vert_dict[i - surf].adjacent.has_key(i)):
            del(aGraph.vert_dict[i -surf].adjacent[i])
        if (i < (surf * DEPTH - surf) and aGraph.vert_dict[i + surf].adjacent.has_key(i)):
            del(aGraph.vert_dict[i + surf].adjacent[i])
        if (a % WIDTH and aGraph.vert_dict[i - 1].adjacent.has_key(i)):
            del(aGraph.vert_dict[i - 1].adjacent[i])
        if (a % WIDTH != (WIDTH - 1) and aGraph.vert_dict[i + 1].adjacent.has_key(i)):
            del(aGraph.vert_dict[i + 1].adjacent[i])
        if (a > WIDTH and aGraph.vert_dict[i - WIDTH].adjacent.has_key(i)):
            del(aGraph.vert_dict[i - WIDTH].adjacent[i])
        if (a < (surf - WIDTH) and aGraph.vert_dict[i + WIDTH].adjacent.has_key(i)):
            del(aGraph.vert_dict[i + WIDTH].adjacent[i])

def apply_path(aGraph, end, p):
    # Compute path.
    target = aGraph.vert_dict[end]
    path = []
    path.append(target.id)
    shortest(target, path)
    print path

    # Delete connections to nodes in the path.
    disconnect_vertex(aGraph, path)

    for i in path:
        aGraph.vert_dict[i].path = p

    # Prepare graph for next search.
    for v in aGraph:
        v.distance = sys.maxint
        v.visited = False
        v.previous = None

def connect_Graph(g):
    # Connects all vertices of the graph in a grid-like manner.
    n = HEIGHT * WIDTH * DEPTH
    for i in range(n):
        g.add_vertex(i)

    # Create graph
    for i in range(n):
        surf = WIDTH * HEIGHT
        a = i % surf
        current = g.vert_dict[i]

        # In / Out connections
        if (i >= surf):
            current.add_neighbor(i - surf)
        if (i < (surf * DEPTH - surf)):
            current.add_neighbor(i + surf)
        # Left / Right / Up / Down
        if (a % WIDTH):
            current.add_neighbor(i - 1)
        if (a % WIDTH != (WIDTH - 1)):
            current.add_neighbor(i + 1)
        if (a > WIDTH):
            current.add_neighbor(i - WIDTH)
        if (a < (surf - WIDTH)):
            current.add_neighbor(i + WIDTH)

if __name__ == '__main__':
    """
    CHIPS AND CIRCUITS first print
    """

    from data.config1 import width, height, gates
    from netlist1 import netlist
    WIDTH = width
    HEIGHT = height
    DEPTH = 8

    # # DEBUG
    # netlist = [(0, 4)]
    
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
    p = 0
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
        dijkstra(g, begin, end)
        apply_path(g, end.id, p)
        p += 1

        elapsed_time = time.time() - start_time
        print 'time: ' + str(elapsed_time)
        # import IPython; IPython.embed()

    import IPython; IPython.embed()
