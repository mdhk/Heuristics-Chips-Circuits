from config1 import width, height, gates

depth = 1

grid = [[[0 for z in range(depth)] for x in range(width)] for y in range(height)]

def set_gates(gates):
    for gate in gates:
         grid[gate[1]][gate[0]] = 1


set_gates(gates)

for x in range(len(grid)):
    print grid[x]

