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
 
def initGrid(width,height):
    # Define some colors
    WHITE = (255, 255, 255)
    
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

    WHITE = (255, 255, 255)
    PATH = (randint(0, 255), randint(0, 255), randint(0, 255))

    MARGIN = 5;
    WIDTH = 20;
    HEIGHT = 20;

    # grid = [[[0 for c in range(DEPTH)] for b in range(WIDTH)] for a in range(HEIGHT)]
    # Draw the grid
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            color = WHITE
            for z in [depth]:    
                #  grid[height][width][depth]
                if grid[y][x][z] != 0:
                    if grid[y][x][z] == 1:
                        grid[y][x][z] = PATH
                        color = grid[y][x][z]
                        pygame.draw.rect(screen,color,
                                 [(MARGIN + WIDTH) * x + MARGIN,
                                  (MARGIN + HEIGHT) * y + MARGIN,
                                  WIDTH,HEIGHT])
     
    # Limit to 60 frames per second
    # clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
# pygame.quit()
