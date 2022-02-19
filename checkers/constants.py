import pygame

WIDTH, HEIGHT = 800,800 # size of the window
ROWS,COLS = 8,8 # number of rows and columns of the board
SQUARE_SIZE = WIDTH//COLS

BLACK = (0,0,0) # RGB values for the color black
WHITE = (255,255,255) # RGB values for the color white
RED = (255,0,0) # RGB values for the color red
BLUE = (0,0,255) # RGB values for the color blue

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (45, 25))

