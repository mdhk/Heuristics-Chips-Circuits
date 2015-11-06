"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame
 
def initGrid(width,height):
    # Define some colors
    BLACK = (0, 0, 0)
    
    # This sets the margin between each cell
    MARGIN = 5
 
    # Initialize pygame
    pygame.init()
 
    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [width * 27, height * 25]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    
    # Set title of screen
    pygame.display.set_caption("Chips and Circuits")
    
    # Set the screen background
    screen.fill(BLACK)

    return screen;
 
def drawGrid(grid, screen, Gate):

    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    MARGIN = 5;
    WIDTH = 20;
    HEIGHT = 20;

    # Draw the grid
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            color = WHITE
            # import IPython; IPython.embed()
            # if grid[row][column] != [0,0,0,0,0,0,0,0]:
            if isinstance(grid[row][column][0], Gate):
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])
 
    # Limit to 60 frames per second
    # clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
# pygame.quit()
