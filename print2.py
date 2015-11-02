"""
Info for print 1
Heuristics, Chips & Circuits, Fall 2015
HaMaMa
"""

# Grid width and height (starting from zero).  
height = 16 
width = 17

# Gate coordinates, template: gate_x, gate_y
import csv
gates = []
with open('print2.csv', 'rb') as csvfile:
    # Without QUOTE_NONNUMERIC the numbers become strings
    csvfile = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    for row in csvfile:
        gates.append(row)


print gates
