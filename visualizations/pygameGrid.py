"""
 This script requires pygame to visualize a single layer of the grid at a time.
 allVisualization will allow the user to run the visualization with a single
 command. 

 source:
 http://simpson.edu/computer-science/
"""
import pygame
from random import randint
 
WHITE = (255, 255, 255)

def initGrid(width,height):
    # Define some colors
    
    # This sets the margin between each cell
    MARGIN = 5
 
    # Initialize pygame
    pygame.init()
 
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [width * 25 + 5, height * 25 + 5]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    
    # Set title of screen
    pygame.display.set_caption("Chips and Circuits")
    
    # Set the screen background
    screen.fill(WHITE)

    return screen;
 
def drawGrid(grid, screen, depth):

    # Compute a random color for a new path to be displayed.
    randColor = (randint(0, 254), randint(0, 255), randint(0, 255))

    MARGIN = 5;
    WIDTH = 20;
    HEIGHT = 20;
    DEPTH = 8;

    # Fill the grid with a color at the required positions. 
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            for z in range(DEPTH):  
                if grid[y][x][depth] != (255, 0, 0):
                    pygame.draw.rect(screen, grid[y][x][depth],
                            [(MARGIN + WIDTH) * x + MARGIN,
                                (MARGIN + HEIGHT) * y + MARGIN,
                                WIDTH,HEIGHT],1)  
                if grid[y][x][z] == 1:
                    grid[y][x][z] = randColor

    # Draw the (entire) grid.
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x][depth] != 0:
                if grid[y][x][depth] == (255, 0, 0):
                    pygame.draw.circle(screen, grid[y][x][depth],[(MARGIN +
                        WIDTH) * x + 3 * MARGIN, (MARGIN + HEIGHT) * y + 3 * MARGIN],
                        10, 0)
                else:
                    pygame.draw.rect(screen, grid[y][x][depth],
                        [(MARGIN + WIDTH) * x + MARGIN,
                            (MARGIN + HEIGHT) * y + MARGIN,
                            WIDTH,HEIGHT])
 
    pygame.display.flip()

"""
allVisualization allows the complete visualization to be created for a given
(preferably finished) grid g. 
"""
def allVisualization(g, gates, TOFIND):
    import random

    # Initialize visualization.
    screen = initGrid(g.WIDTH, g.HEIGHT)
    grid = [[[0 for c in range(g.DEPTH)] for b in range(g.WIDTH)] for a in
            range(g.HEIGHT)]
    # Color all gates bright red.
    for i in gates:
        grid[i[1]][i[0]][0] = (255, 0, 0)
    depth = 0 

    for p in range(TOFIND):
        randcolor = (random.randint(0, 254), random.randint(0, 255), random.randint(0, 255))
        for v in g:
            if v.path == p and not v.gate:
                grid[v.y][v.x][v.z] = randcolor
                drawGrid(grid, screen, depth)

    # import IPython; IPython.embed()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Visualize the layer up or down from current (left and right click
            # respectively).
            if event.button == 1 and depth != 7:
                screen.fill([255,255,255])
                depth += 1
                drawGrid(grid, screen, depth)
                print 'Showing layer: ' + str(depth)
            if event.button == 3 and depth != 0:
                screen.fill([255,255,255])
                depth -= 1
                drawGrid(grid, screen, depth)
                print 'Showing layer: ' + str(depth)
