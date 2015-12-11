def convert(g):
    import json, core, random

    feed = []
    pathIDs = []

    for v in g:
        if v.path and v.path not in pathIDs:
            pathIDs.append(v.path)

    print pathIDs
    for i in pathIDs:
        print i
        points = []
        vertices = []
        path = []
        gate = 0

        for v in g:
            if v.path == i:
                vertices.append(v.id)
                if v.gate == True:
                    gate = v.id

        # NOT ALL PATHS ARE FOUND! BUG ALERT!
        # Gates do not have paths: therefore these will not be found
        if not gate:
            gate = random.choice(vertices)

        # import IPython; IPython.embed();

        cur = gate
        vertices.remove(gate)
        path.append(gate)
        for n in range(len(vertices)):
            for nb in core.computeNeighbors(g, cur):
                if nb in vertices:
                    path.append(nb)
                    vertices.remove(nb)
                    cur = nb
                    break

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
