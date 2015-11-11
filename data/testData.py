# testData
# Heuristics, Chips & Circuits, Fall 2015
# HaMaMa
import numpy 

# grid width and height
width = 5
height = 6

# gate coordinates, template: [gate_number, gate_x, gate_y]
gates = [
		[1, 1],
		[3, 2],
        [1, 3],
        [2, 4],
        ]

# gate 0 = [1,1] .. gate 3= [2,4], Tussen de volgende gates loopt er een pad:
netlist = [(0,1),(0,2),(2,3),(3,1)]