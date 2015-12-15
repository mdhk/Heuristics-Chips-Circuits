def convert(g):
    # This script assumes that all paths in the netlist have been found.
    import json, core, random

    feed = []
    pathIDs = []

    # This assumes that not all paths are found. 
    # for v in g:
    #     if v.path and v.path not in pathIDs:
    #         pathIDs.append(v.path)
    import IPython; IPython.embed();

    N = len(g.netlist)
    for i in range(1,N+1):
        # print i
        points = []
        vertices = []
        path = []
        gate = 0

        for v in g:
            if v.path == i and not v.gate:
                vertices.append(v.id)


        # import IPython; IPython.embed();

        # The first gate is where the tracing starts
        cur = g.netlist[i - 1][0]
        path.append(cur)
        for n in range(len(vertices)):
            for nb in core.computeNeighbors(g, cur):
                if nb in vertices:
                    path.append(nb)
                    vertices.remove(nb)
                    cur = nb
                    break
        path.append(g.netlist[i - 1][1])

        for p in path:
            d = {}
            cur = g.vertDict[p]

            # d['x'] = cur.x * 10
            # d['y'] = cur.y * 10
            # d['z'] = cur.z * 10

            # Different orientation
            d['x'] = cur.y * 10
            d['y'] = cur.z * -10
            d['z'] = cur.x * 10

            points.append(d)

        feed.append(points)

    with open('jsonThreejs.json', 'w') as outfile:
        json.dump(feed, outfile)
    # import IPython; IPython.embed();
