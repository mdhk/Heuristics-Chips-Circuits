"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
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

    randColor = (randint(0, 200), randint(0, 255), randint(0, 255))

    MARGIN = 5;
    WIDTH = 20;
    HEIGHT = 20;
    DEPTH = 8;

    # Fill the grid. 
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            for z in range(DEPTH):    
                if grid[y][x][z] == 1:
                    grid[y][x][z] = randColor

    # Draw the (entire) grid.
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x][depth] != 0:
                pygame.draw.rect(screen, grid[y][x][depth],
                        [(MARGIN + WIDTH) * x + MARGIN,
                            (MARGIN + HEIGHT) * y + MARGIN,
                            WIDTH,HEIGHT])
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
# pygame.quit()
