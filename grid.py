width = 18
height = 13
depth = 1

grid = [[[0 for z in range(depth)]for y in range(height)] for x in range(width)]

for x in range(len(grid)):
    print grid[x]
