from config2 import width, height, gates

depth = 1

grid = [[[0 for z in range(depth)] for x in range(width)] for y in range(height)]

def set_gates(gates):
    for gate in range(len(gates)):
        gate_x = gates[gate][0]
        gate_y = gates[gate][1]
        grid[gate_y][gate_x] = gates.index(gate) + 1

set_gates(gates)

for x in range(len(grid)):
    print grid[x]

# class Gate
